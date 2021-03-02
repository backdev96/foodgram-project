from django.contrib import admin


# Register your models here.
from .models import Ingredient, Recipe, User
from django.contrib.auth import get_user_model


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'unit')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author')
    search_field = ('author', 'title',)
    empty_value_display = '-пусто-'



admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)