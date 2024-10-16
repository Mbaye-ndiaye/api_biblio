from django.db import models
from django.core.validators import MinValueValidator

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField(help_text="Description du livre", blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.0)], help_text="Prix du livre")
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True, help_text="Image de couverture")
    total_copies = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Nombre total d'exemplaires")
    available_copies = models.PositiveIntegerField(validators=[MinValueValidator(0)], help_text="Nombre d'exemplaires disponibles")

    def __str__(self):
        return self.title
