# Generated by Django 5.1.1 on 2024-10-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0015_customuser_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
