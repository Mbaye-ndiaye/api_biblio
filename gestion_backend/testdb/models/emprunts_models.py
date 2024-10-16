from django.db import models
from .livres import Livre
from .member import Member
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.utils import timezone


# Cheikh Gueye : Création du modèle 'Emprunt' pour emprunter les livres
class Emprunt(models.Model):
    membre = models.ForeignKey(Member, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_echeance = models.DateTimeField()
    is_returned = models.BooleanField(default=False)
    membre_nom = models.CharField(max_length=100, blank=True, null=True)
    livre_titre = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Lors de la création d'un nouvel emprunt
            if self.livre.is_available():
                self.livre.emprunts_en_cours += 1
                self.livre.copies_restantes -= 1
                self.livre.save()  # Sauvegarder pour mettre à jour les valeurs
                # Mettre à jour les champs des noms
                self.membre_nom = f"{self.membre.prenom} {self.membre.nom}"
                self.livre_titre = self.livre.titre
            else:
                raise ValueError("Le livre n'est pas disponible.")
        else:  # Lors de la mise à jour d'un emprunt
            if self.is_returned and not self.livre.is_available():  # Vérifier si c'est un retour
                # Réinitialiser les valeurs
                self.livre.emprunts_en_cours -= 1
                self.livre.copies_restantes += 1  # Réinitialiser le nombre de copies restantes
                self.livre.save()
        
        super().save(*args, **kwargs)

    def check_auto_return(self):
        if not self.is_returned and self.date_echeance < timezone.now():
            self.is_returned = True
            self.livre.emprunts_en_cours -= 1
            self.livre.save()
            self.save()  # Enregistre le retour automatique

    def __str__(self):
        return f"{self.membre} - {self.livre} ({'Rendu' if self.is_returned else 'Non Rendu'})"

@receiver(post_save, sender=Emprunt)
def update_livre_counts(sender, instance, created, **kwargs):
    livre = instance.livre

    if created:  # Si un nouvel emprunt a été créé
        livre.emprunts_en_cours += 1
        livre.copies_restantes -= 1
    else:  # Si l'emprunt a été mis à jour (par exemple, lors d'un retour)
        if instance.is_returned:
            livre.emprunts_en_cours -= 1
            livre.copies_restantes += 1

    livre.save()  # Sauvegarder les changements dans le modèle Livre

