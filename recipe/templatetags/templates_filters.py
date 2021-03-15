from django import template

from recipe.models import ShoppingList, Favourite, Follow, Recipe

register = template.Library()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')


@register.filter(name='get_filter_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()
    if tag.slug in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.slug)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.slug)
    return new_request.urlencode()


@register.filter(name='is_shop')
def is_shop(recipe, user):
    return ShoppingList.objects.filter(user=user, recipe=recipe).exists()

@register.filter(name='is_favorite')
def is_favorite(recipe, user):
    return Favourite.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='is_follow')
def is_follow(author, user):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter(name='get_recipes')
def get_recipes(author):
    return Recipe.objects.select_related("author").filter(author=author)[:3]


@register.filter(name='get_count_recipes')
def get_count_recipes(author):
    count = author.recipes.count() - 3
    if count < 1:
        return False

    if count % 10 == 1 and count % 100 != 11:
        end = 'рецепт'
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        end = 'рецепта'
    else:
        end = 'рецептов'

    return f'Еще {count} {end}...'


@register.filter(name='shopping_count')
def shopping_count(request, user_id):
    return ShoppingList.objects.filter(user=user_id).count()
