# Generated by Django 4.2.6 on 2025-04-23 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0006_utilisateur_sexe'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoring',
            name='latitude_du_lieu_de_monitoring',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='monitoring',
            name='longitude_du_lieu_de_monitoring',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='planting',
            name='latitude_du_lieu_de_planting',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='planting',
            name='longitude_du_lieu_de_planting',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
