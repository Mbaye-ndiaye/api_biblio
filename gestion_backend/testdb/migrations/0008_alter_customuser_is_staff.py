# Generated by Django 5.1.1 on 2024-10-08 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0007_customuser_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]