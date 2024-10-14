from rest_framework import serializers
from .models import Member, CustomUser, Livre, Emprunt

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'telephone')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            telephone=validated_data['telephone'],
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            'id', 
            'prenom', 
            'nom', 
            'telephone', 
            'email'
        ]


class LivreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livre
        fields = [
            'id', 
            'titre', 
            'auteur', 
            'date_de_publication', 
            'categorie', 
            'nbr_copies_dispo', 
            'total_copies', 
            'couverture'
        ]


class EmpruntSerializer(serializers.ModelSerializer):
    livre_details = LivreSerializer(source='livre', read_only=True)
    membre_details = MemberSerializer(source='membre', read_only=True)

    membre_nom = serializers.CharField(source='membre.nom', read_only=True)
    livre_titre = serializers.CharField(source='livre.titre', read_only=True)

    class Meta:
        model = Emprunt
        fields = [
            'id', 
            'membre', 
            'livre', 
            'date_emprunt', 
            'date_echeance', 
            'is_returned', 
            'livre_details', 
            'membre_details',
            'membre_nom',
            'livre_titre',
        ]
