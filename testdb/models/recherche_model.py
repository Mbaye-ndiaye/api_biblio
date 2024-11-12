from django.db import models

class Livre(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    date_publication = models.DateField()

    def __str__(self):
        return self.titre
