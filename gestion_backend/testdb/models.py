from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

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