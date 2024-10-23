from rest_framework import serializers
from ..models.emprunt_model import Emprunt
from ..models.member_models import Member
from ..models.book import Book
from django.contrib.auth import get_user_model

class EmpruntSerializer(serializers.ModelSerializer):
    livre_nom = serializers.CharField(source='livre.title', read_only=True)
    membre_nom = serializers.CharField(source='membre.nom', read_only=True)

    class Meta:
        model = Emprunt
        fields = ['id', 'livre', 'livre_nom', 'membre', 'membre_nom', 'date_emprunt', 'date_retour', 'rendu']
        read_only_fields = ['date_emprunt', 'rendu']

    def create(self, validated_data):
        livre = validated_data['livre']
        if livre.available_copies <= 0:
            raise serializers.ValidationError("Aucune copie disponible pour ce livre.")

        livre.available_copies -= 1
        livre.save()

        membre = validated_data['membre']
    # Accéder au modèle Member si nécessaire
        try:
           membre_instance = Member.objects.get(user=membre)
           validated_data['membre_nom'] = membre_instance.nom + " " + membre_instance.prenom
        except Member.DoesNotExist:
            raise serializers.ValidationError("Membre introuvable.")

        validated_data['livre_nom'] = livre.title

        return super().create(validated_data)

