from django.db import models

# Cheikh Gueye : Création du modèle 'Livre' pour les livres
class Livre(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    date_de_publication = models.DateField()
    categorie = models.CharField(max_length=100)
    total_copies = models.IntegerField(default=0)  # Total de copies ajoutées
    emprunts_en_cours = models.IntegerField(default=0)  # Par défaut, 0 livres empruntés
    copies_restantes = models.IntegerField(default=0)
    couverture = models.ImageField(upload_to='covers/', blank=True, null=True)

    @property
    def nbr_copies_dispo(self):
        # Stock disponible = total - nombre de livres empruntés
        return self.total_copies - self.emprunts_en_cours

    def is_available(self):
        # Vérifie s'il reste des livres disponibles
        return self.nbr_copies_dispo > 0
    
    def save(self, *args, **kwargs):
        # Mettre à jour copies_restantes chaque fois que le livre est sauvegardé
        self.copies_restantes = self.total_copies - self.emprunts_en_cours
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre
