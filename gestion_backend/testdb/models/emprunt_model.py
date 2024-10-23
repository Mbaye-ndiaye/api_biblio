from django.db import models
from .book import Book
from django.conf import settings
from django.utils import timezone

class Emprunt(models.Model):
    livre = models.ForeignKey(Book, on_delete=models.CASCADE)
    membre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membre_nom = models.CharField(max_length=255, blank=True, null=True)
    livre_nom = models.CharField(max_length=255, blank=True, null=True) 
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour = models.DateTimeField(null=True, blank=True)
    rendu = models.BooleanField(default=False)

    def __str__(self):
        return f"Emprunt de {self.livre.title} par {self.membre.username}"
