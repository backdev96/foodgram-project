# Generated by Django 3.1.3 on 2021-03-17 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='color',
            new_name='colour',
        ),
    ]