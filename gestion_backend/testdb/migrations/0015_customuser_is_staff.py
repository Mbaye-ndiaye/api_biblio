# Generated by Django 5.1.1 on 2024-10-09 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0014_alter_customuser_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
