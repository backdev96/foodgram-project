# Generated by Django 3.1.3 on 2021-03-20 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20210320_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientrecipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
    ]
