# Generated by Django 5.1.1 on 2024-10-09 14:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Emprunt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_emprunt', models.DateTimeField(auto_now_add=True)),
                ('date_de_retour', models.DateTimeField(blank=True, null=True)),
                ('date_echeance', models.DateTimeField()),
                ('is_returned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Livre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('auteur', models.CharField(max_length=255)),
                ('date_de_publication', models.DateField()),
                ('categorie', models.CharField(max_length=100)),
                ('nbr_copies_dispo', models.IntegerField(default=0)),
                ('total_copies', models.IntegerField(default=0)),
                ('couverture', models.ImageField(blank=True, null=True, upload_to='covers/')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=50)),
                ('nom', models.CharField(max_length=50)),
                ('telephone', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.AddField(
            model_name='emprunt',
            name='livre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdb.livre'),
        ),
        migrations.AddField(
            model_name='emprunt',
            name='membre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testdb.member'),
        ),
    ]
