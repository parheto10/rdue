# Generated by Django 4.2.6 on 2024-11-07 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0002_recolteproducteur_check_gap'),
    ]

    operations = [
        migrations.AddField(
            model_name='recolteproducteur',
            name='gap',
            field=models.IntegerField(default=0),
        ),
    ]
