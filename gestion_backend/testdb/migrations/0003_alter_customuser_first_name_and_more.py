# Generated by Django 5.1.1 on 2024-10-08 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0002_remove_customuser_nom_remove_customuser_prenom_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]