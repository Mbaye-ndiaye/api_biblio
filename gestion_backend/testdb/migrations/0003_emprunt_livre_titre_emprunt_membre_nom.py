# Generated by Django 5.1.1 on 2024-10-12 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0002_remove_emprunt_date_de_retour'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprunt',
            name='livre_titre',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='emprunt',
            name='membre_nom',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
