from django.shortcuts import get_object_or_404, render, redirect
from .models import Recipe, User, Follow, Favourite, ShoppingList
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .utils import food_time_filter, get_ingredients

from .forms import RecipeForm

def index(request):
    recipe = Recipe.objects.select_related(
        'author').order_by('-pub_date').all()
    recipe_list, food_time = food_time_filter(request, recipe)

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'index.html', {
            'page': page,
            'paginator': paginator,
            'food_time': food_time
        }
    )


def recipe_view(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, 'singlePage.html', {'recipe': recipe})


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
    form = RecipeForm(request.POST, files=request.FILES or None)
    if request.method != 'POST':
        return render(request, 'formRecipe.html', {'form': form})
    if form.is_valid():
        recipe_new = form.save(commit=False)
        recipe_new.author = request.user
        recipe_new.save()
        return redirect('index')
    return render(request, 'formRecipe.html', {'form' : form})


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
    authors = User.objects.filter(following__user=request.user)
    recipes = Recipe.objects.filter(
        author__in=authors).order_by('-pub_date')
    count_recipes = {}
    for author in authors:
        recipes_count[author.username] = Recipe.objects.filter(
            author=author).count()-3
    recipes_for_print = []
    for author in authors:
        recipes_for_print.append(Recipe.objects.filter(
            author=author).order_by('-pub_date')[:3])
    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "authors": authors,
        "count_recipes": count_recipes,
        "recipes_for_print": recipes_for_print
    }
    return render(request, "myFollow.html", context)

@login_required
def add_to_cart(request):
    pass

    
@login_required
def add_to_favourites(request, recipe_id):
    recipes = Recipe.objects.filter(author__following__user=request.user)
    paginator = Paginator(recipes, 6)
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
    return render(request, "myFollow.html", context)


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
