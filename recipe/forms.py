from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Recipe, IngredientForRecipe


class RecipeForm(forms.ModelForm):


    class Meta:
        model = Recipe
        fields = [
            'title',
            'breakfast',
            'lunch',
            'dinner',
            'image',
            'description',
            'cooking_time']
        widgets = {
            'tag': CheckboxSelectMultiple(),
        }

class IngredientForRecipeForm(forms.ModelForm):

    class Meta:
        model = IngredientForRecipe
        fields = ['amount',]
