from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


# Cheikh Gueye : Création du modèle 'Member' pour les membres
class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    total_copies = models.IntegerField(default=0)  # Total de copies ajoutées
    emprunts_en_cours = models.IntegerField(default=0)  # Par défaut, 0 livres empruntés
    couverture = models.ImageField(upload_to='covers/', blank=True, null=True)

    @property
    def nbr_copies_dispo(self):
        # Stock disponible = total - nombre de livres empruntés
        return self.total_copies - self.emprunts_en_cours

    def is_available(self):
        # Vérifie s'il reste des livres disponibles
        return self.nbr_copies_dispo > 0

    def __str__(self):
        return self.titr


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
                self.livre.save()
                
                # Mettre à jour les champs des noms
                self.membre_nom = f"{self.membre.prenom} {self.membre.nom}"
                self.livre_titre = self.livre.titre
            else:
                raise ValueError("Le livre n'est pas disponible.")
        elif self.is_returned:  # Lors du retour d'un emprunt
            self.livre.emprunts_en_cours -= 1
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

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format: '999999999'"
    )
    telephone = models.CharField(validators=[phone_regex], max_length=17)
    is_staff = models.BooleanField(default=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True, null=True)
    is_superuser = models.BooleanField(default=True, null=True)
    is_admin = models.BooleanField(default=False, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telephone']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
