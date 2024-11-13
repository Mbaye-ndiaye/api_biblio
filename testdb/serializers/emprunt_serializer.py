from rest_framework import serializers
from ..models.emprunt_model import Emprunt
from ..models.book import Book
from django.contrib.auth import get_user_model

class EmpruntSerializer(serializers.ModelSerializer):
    livre_nom = serializers.CharField(source='livre.title', read_only=True)
    membre_nom = serializers.CharField(source='membre.get_full_name', read_only=True)  # Utilisation de `get_full_name`

    class Meta:
        model = Emprunt
        fields = ['id', 'livre', 'livre_nom', 'membre', 'membre_nom', 'date_emprunt', 'date_retour', 'rendu']
        read_only_fields = ['date_emprunt', 'rendu']

    def create(self, validated_data):
        livre = validated_data['livre']
        if livre.available_copies <= 0:
            raise serializers.ValidationError("Aucune copie disponible pour ce livre.")

        # Mise à jour des copies disponibles du livre
        livre.available_copies -= 1
        livre.save()

        # Utilisation de l'utilisateur authentifié
        user = self.context['request'].user  # Récupère l'utilisateur connecté
        validated_data['membre'] = user

        # Récupérer le nom complet de l'utilisateur
        validated_data['membre_nom'] = user.get_full_name()  # Utilise `get_full_name` de l'utilisateur

        validated_data['livre_nom'] = livre.title

        return super().create(validated_data)
