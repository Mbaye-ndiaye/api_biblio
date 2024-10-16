# Generated by Django 5.1.1 on 2024-10-16 14:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, help_text='Description du livre', null=True)),
                ('price', models.DecimalField(decimal_places=2, help_text='Prix du livre', max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('cover_image', models.ImageField(blank=True, help_text='Image de couverture', null=True, upload_to='book_covers/')),
                ('total_copies', models.PositiveIntegerField(help_text="Nombre total d'exemplaires", validators=[django.core.validators.MinValueValidator(1)])),
                ('available_copies', models.PositiveIntegerField(help_text="Nombre d'exemplaires disponibles", validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]
