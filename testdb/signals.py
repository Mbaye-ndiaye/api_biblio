from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models.member_models import Member

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_member(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance, prenom=instance.first_name, nom=instance.last_name)
