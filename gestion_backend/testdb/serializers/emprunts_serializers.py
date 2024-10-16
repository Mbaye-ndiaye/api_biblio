from rest_framework import serializers
from .livres_serializers import LivreSerializer
from .member_serializers import MemberSerializer
from ..models import Emprunt

class EmpruntSerializer(serializers.ModelSerializer):
    livre_details = LivreSerializer(source='livre', read_only=True)
    membre_details = MemberSerializer(source='membre', read_only=True)

    membre_nom = serializers.CharField(source='membre.nom', read_only=True)
    livre_titre = serializers.CharField(source='livre.titre', read_only=True)

    class Meta:
        model = Emprunt
        fields = ['id', 'membre', 'livre', 'date_emprunt', 'date_echeance', 'is_returned', 'livre_details', 'membre_details', 'membre_nom', 'livre_titre']