# Generated by Django 4.0.6 on 2022-08-12 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('techbro', '0011_showcase_dish_showcase1_dish_showcase2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='showcase1',
        ),
        migrations.RemoveField(
            model_name='dish',
            name='showcase2',
        ),
        migrations.RemoveField(
            model_name='dish',
            name='showcase3',
        ),
    ]