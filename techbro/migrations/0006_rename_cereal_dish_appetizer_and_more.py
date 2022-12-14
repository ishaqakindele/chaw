# Generated by Django 4.0.6 on 2022-08-05 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techbro', '0005_alter_dish_cereal_alter_dish_pudding_alter_dish_tea'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dish',
            old_name='cereal',
            new_name='appetizer',
        ),
        migrations.RenameField(
            model_name='dish',
            old_name='pudding',
            new_name='breakfast',
        ),
        migrations.RenameField(
            model_name='dish',
            old_name='tea',
            new_name='dessert',
        ),
        migrations.AddField(
            model_name='dish',
            name='dinner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dish',
            name='drink',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dish',
            name='lunch',
            field=models.BooleanField(default=False),
        ),
    ]
