from django.db import models

class Admin(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()

# Create your models here.
