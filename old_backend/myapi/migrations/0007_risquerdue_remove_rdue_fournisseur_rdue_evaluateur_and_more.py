# Generated by Django 4.2.6 on 2023-12-04 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0006_alter_rdue_action_comm_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RisqueRDUE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='rdue',
            name='fournisseur',
        ),
        migrations.AddField(
            model_name='rdue',
            name='evaluateur',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='parcelle',
            name='risque',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapi.risquerdue'),
        ),
    ]