from rest_framework import serializers
from ..models import Livre

class LivreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livre
        fields = ['id', 'titre', 'auteur', 'date_de_publication', 'categorie', 'nbr_copies_dispo', 'total_copies', 'couverture']