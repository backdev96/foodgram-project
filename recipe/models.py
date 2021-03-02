from django.db import models
from django.contrib.auth import get_user_model
from django.forms.widgets import TextInput
from django.utils.dateparse import parse_duration
from taggit.managers import TaggableManager

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    unit = models.CharField(max_length=50, blank=False)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='date published', auto_now_add=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Image')
    description = models.TextField(verbose_name='Текст', help_text='Text description')
    ingredients = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='recipe', verbose_name='Ingriedient', help_text='Choose your ingridients')
    slug = models.SlugField(max_length=50, unique=True, blank=False, null=True)
    cooking_time = models.PositiveIntegerField(blank=False)
    breakfast = models.BooleanField(
        default=False, verbose_name='Завтрак'
    )
    lunch = models.BooleanField(
        default=False, verbose_name='Обед'
    )
    dinner = models.BooleanField(
        default=False, verbose_name='Ужин'
    )

    def __str__(self):
        short_description = self.description[:10]
        return f'{self.author} - {self.pub_date:%d %b-%Y} - {short_description}'


class Follow(models.Model):
    '''Follow model'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='follow')
    following = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='following')
    unique_together = ('user', 'following')

    def __str__(self):
        return f'Follows {self.user}'


class IngredientForRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient')
    amount = models.PositiveSmallIntegerField(verbose_name='Amount', default=0, blank=True, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.ingredient} for {self.recipe}'


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopping_list',
                             verbose_name='User')
    recipe = models.ManyToManyField(
        Recipe, related_name='shopping_list', verbose_name='Recipes', blank=True)

    def __str__(self):
        return f'Shopping list {self.user}'


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourite_user')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favourite_recipe')

    def __str__(self):
        return f'Favourite recipes {self.user}'
