# Generated by Django 4.2.15 on 2024-08-27 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_ingredients_ingredients_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='ExpiryDate',
            field=models.DateField(),
        ),
    ]
