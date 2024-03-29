# Generated by Django 3.1.3 on 2021-03-20 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20210319_2123'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredient',
            new_name='Ingredients',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredient',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.IngredientRecipe', to='recipes.Ingredients'),
        ),
    ]
