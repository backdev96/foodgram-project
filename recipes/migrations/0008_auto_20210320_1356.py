# Generated by Django 3.1.3 on 2021-03-20 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20210320_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientrecipe',
            old_name='ingredients',
            new_name='ingredient',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredients',
            new_name='ingredient',
        ),
    ]
