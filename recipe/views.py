from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe, User, Follow, Favourite, ShoppingList, Ingredient, IngredientForRecipe
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .utils import food_time_filter, get_ingredients
from foodgram.settings import ITEMS_FOR_PAGINATOR
from .forms import RecipeForm

def index(request):
    recipe = Recipe.objects.select_related(
        'author').order_by('-pub_date').all()
    recipe_list, food_time = food_time_filter(request, recipe)

    paginator = Paginator(recipe_list, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'index.html', {
            'page': page,
            'paginator': paginator,
            'food_time': food_time
        }
    )


def recipe_view(request, recipe_id, username):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    username = get_object_or_404(User, username=username)
    ingredients = IngredientForRecipe.objects.filter(recipe=recipe)
    return render(request, 'singlePage.html', {'username': username, 
                                                'recipe': recipe, 
                                                'ingredients': ingredients})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes_count = Recipe.objects.filter(author=author).count()
    recipe = Recipe.objects.filter(author=author)
    paginator = Paginator(recipe, 6)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'singlePage.html', {
        'page': page,
        'paginator': paginator,
        'recipes_count': recipes_count,
        'author': author
    })


@login_required
def recipe_new(request):
    user = User.objects.get(username=request.user)

    if request.method == 'POST':
        ingr = get_ingredients(request)
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        if not ingr:
            form.add_error(None, 'Добавьте ингредиенты')

        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            for ingr_name, amount in ingr.items():
                ingr_obj = get_object_or_404(Ingredient, title=ingr_name)
                ingr_recipe = IngredientRecipe(
                    ingredient=ingr_obj,
                    recipe=recipe,
                    amount=amount,
                )
                ingr_recipe.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})



@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=username)
    form = RecipeForm(request.POST or None, instance=recipe)
    if form.is_valid():
        form.save()
        return redirect('recipe', username=username, recipe_id=recipe_id)
    return render(request, 'formChangeRecipe.html', {'form': form, 'recipe': recipe})

@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_superuser or request.user == recipe.author:
        recipe.delete()
    return redirect('index')

@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    if user != author:
        follow = Follow.objects.get_or_create(user=user, author=author)
    return redirect('profile', username=username)

@login_required
def profile_unfollow(request, username):
    user = request.user
    author = User.objects.get(username=username)
    follow = Follow.objects.filter(user=user, author=author)
    follow.delete()
    return redirect('profile', username=username)

@login_required
def follow_index(request):
    follow = Follow.objects.filter(user=request.user)
    cnt = {}
    for author in follow:
        amount = Recipe.objects.filter(author=author.author).count()
        cnt[author.author] = amount
    paginator = Paginator(follow, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {
        "page": page,
        "paginator": paginator,
        "cnt": cnt,
    }
    )

@login_required
def add_to_cart(request):
    pass

    
@login_required
def add_to_favourites(request, recipe_id):
    recipes = Recipe.objects.filter(author__following__user=request.user)
    paginator = Paginator(recipes, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'page_number': page_number
    }
    return render(request, "myFollow.html", context)

@login_required
def delete_from_favourites(request, recipe_id):
    user = request.user
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, recipe_id=recipe_id)
    if user != author:
        favourite = Favourite.objects.delete(user=user, recipe=recipe)
    return redirect('singlePage.html', username=username)


@login_required
def favourite_index(request):
    recipes = Favourite.objects.filter(user=request.user)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "recipes": recipes
    }
    return render(request, "follow.html", context)


@login_required
def cart(request):
    shops = get_object_or_404(
        ShoppingList, user=request.user).recipes.order_by('-pub_date')
    return render(request, 'shopList.html', {'shops': shops})


def purchases_add(request):
    recipe_id = json.loads(request.body).get("id")
    recipe = get_object_or_404(Recipe, id=recipe_id)
    shops = ShoppingList.objects.get_or_create(user=request.user)
    shops[0].recipes.add(recipe)
    return JsonResponse({"success": True})


def purchases_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    shops = get_object_or_404(ShoppingList, user=request.user)
    shops.recipes.remove(recipe)
    return JsonResponse({"success": True})


@login_required
def shopping_list(request):
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    return render(
        request,
        'shopList.html',
        {'shopping_list': shopping_list}
    )
