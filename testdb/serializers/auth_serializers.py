# myapp/serializers/auth_serializers.py
from rest_framework import serializers
from ..models.auth_models import CustomUser  

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour afficher les informations d'un utilisateur.

    Ce sérialiseur transforme un objet `CustomUser` en JSON pour la vue des données utilisateur.
    """
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


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'telephone']

        extra_kwargs = {
            'id': {'read_only': True, 'help_text': 'Identifiant unique de l\'utilisateur.'},
            'email': {'help_text': 'Adresse e-mail de l\'utilisateur.'},
            'first_name': {'help_text': 'Prénom de l\'utilisateur.'},
            'last_name': {'help_text': 'Nom de famille de l\'utilisateur.'},
            'telephone': {'help_text': 'Numéro de téléphone de l\'utilisateur.'},
        }
































# # myapp/serializers/auth_serializers.py
# from rest_framework import serializers
# from ..models.auth_models import CustomUser  
# from ..models.member_models import Member
# class UserRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'email', 'password', 'first_name', 'last_name', 'telephone')
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'id': {'read_only': True}
#         }

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             email=validated_data['email'],
#             password=validated_data['password'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             telephone=validated_data['telephone'],
#         )
        
#         # Cheikh Gueye : Créer le membre associé à l'utilisateur inscrit
#         Member.objects.create(
#             user=user,
#             prenom=validated_data['first_name'],
#             nom=validated_data['last_name'],
#             telephone=validated_data['telephone'],
#             email=validated_data['email'],
#         )
#         return user

# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'email', 'first_name', 'last_name', 'telephone']

