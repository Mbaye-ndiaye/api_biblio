from django.db import models
from django.contrib.auth.models import User

# Cheikh Gueye : Création du modèle 'Member' pour les membres
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# Cheikh Gueye : Création du modèle 'Livre' pour les livres
class Livre(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    date_de_publication = models.DateField()
    categorie = models.CharField(max_length=100)
    nbr_copies_dispo = models.IntegerField(default=0)
    total_copies = models.IntegerField(default=0)
    couverture = models.ImageField(upload_to='covers/', blank=True, null=True)

    def is_available(self):
        return self.nbr_copies_dispo > 0

    def __str__(self):
        return self.titre

# Cheikh Gueye : Création du modèle 'Emprunt' pour emprunter les livres
class Emprunt(models.Model):
    membre = models.ForeignKey(Member, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_de_retour = models.DateTimeField(null=True, blank=True)
    date_echeance = models.DateTimeField()
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.membre} - {self.livre} ({'Rendu' if self.is_returned else 'Non Rendu'})"
