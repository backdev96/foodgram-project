from django.contrib import admin
from .models import Ingredient, Recipe, User, ShoppingList, Follow, Favourite
from django.contrib.auth import get_user_model


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'unit')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author')
    search_field = ('author', 'title',)
    empty_value_display = '-пусто-'


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user',)
    search_fields = ('user',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('user',)
    search_fields = ('user',)


class FavouiteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('recipe',)



admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favourite, FavouiteAdmin)
