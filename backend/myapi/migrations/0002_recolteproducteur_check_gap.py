# Generated by Django 4.2.6 on 2024-11-07 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recolteproducteur',
            name='check_gap',
            field=models.BooleanField(default=False),
        ),
    ]
