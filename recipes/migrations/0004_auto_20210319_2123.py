# Generated by Django 3.1.3 on 2021-03-19 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20210319_2117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='followuser',
            options={'ordering': ('user',), 'verbose_name': 'Подписка на автора', 'verbose_name_plural': 'Подписки на авторов'},
        ),
    ]