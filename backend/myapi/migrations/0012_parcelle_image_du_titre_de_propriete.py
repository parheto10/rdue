# Generated by Django 5.0.2 on 2024-05-08 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0011_cooperative_numconnaissement_cooperative_numregistre'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcelle',
            name='image_du_titre_de_propriete',
            field=models.ImageField(null=True, upload_to='titre_de_propriete/'),
        ),
    ]