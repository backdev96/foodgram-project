from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Recipe


class RecipeForm(forms.ModelForm):

    def check_ingredients_existance(self):
        ingredients = list(
            zip(
                self.data.getlist('titleIngredients'),
                self.data.getlist('valueIngredients'),
            ),
        )
        if not ingredients:
            raise forms.ValidationError('Missing ingredients!')

    class Meta:
        model = Recipe
        fields = [
            'title',
            'tags',
            'image',
            'description',
            'cooking_time']
        widgets = {
            'tag': CheckboxSelectMultiple(),
        }
