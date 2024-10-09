# Generated by Django 5.1.1 on 2024-10-08 09:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0005_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
    ]
