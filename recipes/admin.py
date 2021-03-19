from django.contrib import admin
from django.db import models
from django.db.models import Count

from recipes.models import (FollowRecipe, FollowUser, IngredientRecipe,
                            Ingredient, Recipe, ShoppingList, Tag)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author',
        'cooking_time', 'get_favorite_count', 'pub_date'
    )
    list_filter = ('author', 'tags__title')
    search_fields = ('title', 'author__username')
    ordering = ('-pub_date', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(favorite_count=Count('following_recipe'))

    def get_favorite_count(self, obj):
        return obj.favorite_count


admin.site.register(Recipe, RecipesAdmin)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',
                    'description')
    list_filter = ('title',)
    search_fields = ('title',)
    inlines = (IngredientRecipeInline,)


admin.site.register(Ingredient, IngredientsAdmin)


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user',)


admin.site.register(ShoppingList, ShoppingListAdmin)


class FlUsAdmin(admin.ModelAdmin):
    """
    Follow user administration.
    """
    list_display = ('user', 'author')
    list_filter = ('user',)
    search_fields = ('user',)


admin.site.register(FollowUser, FlUsAdmin)


class FlRecAdmin(admin.ModelAdmin):
    """
    Follow recipe administration.
    """
    list_display = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('recipe',)


admin.site.register(FollowRecipe, FlRecAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'colour', 'display_name')
    list_filter = ('title', )


admin.site.register(Tag, TagAdmin)
