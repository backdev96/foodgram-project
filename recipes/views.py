from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import (FollowUser, IngredientRecipe, Ingredients,
                     Recipe, ShoppingList, Tag, User)


TAGS = ['breakfast', 'lunch', 'dinner']


def get_ingredients(request):
    ingredients = {}
    for key in dict(request.POST.items()):
        if 'nameIngredient' in key:
            a = key.split('_')
            ingredients[dict(request.POST.items())[key]] = int(request.POST[
                f'valueIngredient_{a[1]}'])

    return ingredients


@user_passes_test(lambda u: u.is_superuser)
def add_ingredients(self):
    import json

    from django.http import HttpResponse

    with open('ingredients.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    for i in data:
        ingredient = Ingredients(title=i['title'], dimension=i['dimension'])
        ingredient.save()
    return HttpResponse('\n'.join(str(data)))


def index(request):
    tags = request.GET.getlist('tag', [])
    all_tags = Tag.objects.all()
    if not tags:
        recipes = Recipe.objects.select_related(
            'author'
        ).all()
    else:
        recipes = Recipe.objects.filter(
            tags__title__in=tags
        ).select_related(
            'author'
        ).prefetch_related(
            'tags'
        ).distinct()
    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
        }
    )


def profile(request, username):
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
    author = get_object_or_404(User, username=username)
    if tags == ['breakfast', 'lunch', 'dinner']:
        author_recipes = author.recipes.all()
    else:
        author_recipes = author.recipes.filter(
            tags__title__in=tags
        ).prefetch_related('tags').distinct()

    paginator = Paginator(author_recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'author_recipe.html',
        {
            'author': author,
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
        }
    )


def recipe_view(request, recipe_id, username):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    username = get_object_or_404(User, username=username)
    ingredients = IngredientRecipe.objects.filter(recipe=recipe)
    return render(request, 'single_page.html', {'username': username,
             'recipe': recipe, 'ingredients': ingredients})


@login_required
def new_recipe(request):
    user = User.objects.get(username=request.user)
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        ingr = get_ingredients(request)
        recipe = form.save(commit=False)
        recipe.author = user
        recipe.save()
        for ingr_name, amount in ingr.items():
            ingr_obj = get_object_or_404(Ingredients, title=ingr_name)
            ingr_recipe = IngredientRecipe(
                ingredient=ingr_obj,
                recipe=recipe,
                amount=amount,
            )
            ingr_recipe.save()
            if ingr_recipe.amount == 0:
                return redirect('index')
        form.save_m2m()
        return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'form_recipe.html', {'form': form})


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.user != recipe.author:
        return redirect('index')

    if request.method == 'POST':
        form = RecipeForm(request.POST or None,
                          files=request.FILES or None, instance=recipe
                          )
        ingredients = get_ingredients(request)
        if form.is_valid():
            IngredientRecipe.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for item in ingredients:
                IngredientRecipe.objects.create(
                    amount=ingredients[item],
                    ingredient=Ingredients.objects.get(title=f'{item}'),
                    recipe=recipe
                )
            form.save_m2m()
            return redirect('index')

    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)
    return render(request, 'recipe_edit.html',
                  {'form': form, 'recipe': recipe, })

@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_superuser or request.user == recipe.author:
        recipe.delete()
    return redirect('index')


@login_required
def follow_index(request):
    follow = FollowUser.objects.filter(user=request.user)
    cnt = {}
    for author in follow:
        amount = Recipe.objects.filter(author=author.author).count()
        cnt[author.author] = amount
    paginator = Paginator(follow, settings.PAGINATION_PAGE_SIZE_FOR_FOLLOW)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {
        'page': page,
        'paginator': paginator,
        'cnt': cnt,
    }
    )


@login_required
def favorite_index(request):
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
    print(tags)
    if tags == ['breakfast', 'lunch', 'dinner']:
        recipes = Recipe.objects.filter(
            following_recipe__user=request.user,
        ).select_related(
            'author'
        ).prefetch_related(
            'tags'
        ).distinct()
    else:
        recipes = Recipe.objects.filter(
            following_recipe__user=request.user,
            tags__title__in=tags
        ).select_related(
            'author'
        ).prefetch_related(
            'tags'
        ).distinct()
    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'favorite.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
        }
    )


@login_required
def shopping_list(request):
    shopping_list = ShoppingList.objects.filter(user=request.user).all()
    return render(
        request,
        'shopping_list.html',
        {'shopping_list': shopping_list}
    )


@login_required
def download_card(request):
    recipes = Recipe.objects.filter(recipe_shopping_list__user=request.user)
    ingredients = recipes.values(
        'ingredients__title', 'ingredients__dimension'
    ).annotate(
        title=F('ingredients__title'),
        dimension=F('ingredients__dimension'),
        total_amount=Sum('recipe__amount')
    ).order_by(
        ('-total_amount')
    )
    file_data = ''
    for item in ingredients:
        line = ' '.join(str(value) for value in item.values())
        file_data += line + '\n'

    response = HttpResponse(
        file_data, content_type='application/text charset=utf-8'
    )
    response['Content_Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
