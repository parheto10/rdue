# Generated by Django 4.2.6 on 2024-04-11 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0024_alter_detail_engrais_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail_engrais',
            name='engrais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapi.engrais'),
        ),
    ]