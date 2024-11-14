from rest_framework import serializers
from ..models.member_models import Member
from ..models.auth_models import CustomUser

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'prenom', 'nom', 'telephone', 'email']
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'telephone']