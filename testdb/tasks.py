from celery import shared_task
from .models import Emprunt

@shared_task
def check_emprunts():
    emprunts = Emprunt.objects.all()
    for emprunt in emprunts:
        emprunt.check_auto_return()
