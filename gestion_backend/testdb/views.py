# from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from rest_framework import generics
from .models import Member, Livre, Emprunt
from .serializers import MemberSerializer, UserRegistrationSerializer, UserLoginSerializer, LivreSerializer, EmpruntSerializer
from datetime import datetime
from django.utils import timezone
from django.db.models import Count

@api_view(['POST'])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Cheikh Gueye : Créer un membre pour l'utilisateur
        Member.objects.create(
            user=user,
            prenom=request.data['first_name'],
            nom=request.data['last_name'],
            email=user.email,
            telephone=request.data['telephone']
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserRegistrationSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserRegistrationSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({
            'error': 'Email ou mot de passe incorrect'
        }, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({
            'message': 'Déconnexion réussie'
        }, status=status.HTTP_200_OK)
    except Exception:
        return Response({
            'error': 'Token invalide'
        }, status=status.HTTP_400_BAD_REQUEST)

# Cheikh Gueye : Vue pour la liste et création des membres
class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Cheikh Gueye : Vue pour récupérer, modifier ou supprimer un membre spécifique
class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

# Cheikh Gueye : Vue pour la liste et création des livres
class LivreListCreateView(generics.ListCreateAPIView):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer

# Cheikh Gueye : Vue pour récupérer, modifier ou supprimer un livre spécifique
class EmpruntListCreateView(generics.ListCreateAPIView):
    queryset = Emprunt.objects.all()
    serializer_class = EmpruntSerializer

    def create(self, request, *args, **kwargs):
        membre_id = request.data.get('membre')
        livre_id = request.data.get('livre')
        livre = Livre.objects.get(id=livre_id)
        
        # Vérifier si l'utilisateur a déjà 3 emprunts actifs (non retournés)
        active_emprunts = Emprunt.objects.filter(membre_id=membre_id, is_returned=False).count()

        if active_emprunts >= 3:
            return Response({'error': 'Vous ne pouvez pas emprunter plus de trois livres en même temps.'}, status=status.HTTP_400_BAD_REQUEST)

        livre_id = request.data.get('livre')
        livre = Livre.objects.get(id=livre_id)
        
        # Vérifie si le livre est disponible
        if not livre.is_available():
            return Response({'error': 'Le livre n\'est pas disponible pour l\'emprunt.'}, status=status.HTTP_400_BAD_REQUEST)

        # Si tout est bon, appelle la méthode parente pour créer l'emprunt
        return super().create(request, *args, **kwargs)

# Cheikh Gueye : Vue pour récupérer, modifier ou supprimer un emprunt spécifique
class EmpruntDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Emprunt.objects.all()
    serializer_class = EmpruntSerializer
    
class LivreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer

# Cheikh Gueye : Vue pour rendre un livre
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def return_emprunt(request, emprunt_id):
    try:
        emprunt = Emprunt.objects.get(id=emprunt_id)

        # Vérifie que le livre a été emprunté par l'utilisateur connecté
        if emprunt.membre.user.id != request.user.id:
            return Response({'error': 'Vous ne pouvez pas retourner cet emprunt.'}, status=status.HTTP_403_FORBIDDEN)

        # Vérifie si l'emprunt a déjà été retourné
        if emprunt.is_returned:
            return Response({'message': 'Cet emprunt a déjà été retourné.'}, status=status.HTTP_200_OK)

        # Comparer avec timezone.now() pour éviter l'erreur de décalage
        if timezone.now() > emprunt.date_echeance:
            emprunt.is_returned = True
            emprunt.livre.emprunts_en_cours -= 1
            emprunt.livre.save()
            emprunt.save()
            return Response({
                'message': 'Le livre a été retourné automatiquement après dépassement de la date d\'échéance.',
                'emprunt': EmpruntSerializer(emprunt).data
            }, status=status.HTTP_200_OK)

        # Retour manuel
        emprunt.is_returned = True
        emprunt.livre.emprunts_en_cours -= 1
        emprunt.livre.save()
        emprunt.save()
        return Response({
            'message': 'Le livre a été retourné avec succès.',
            'emprunt': EmpruntSerializer(emprunt).data
        }, status=status.HTTP_200_OK)

    except Emprunt.DoesNotExist:
        return Response({'error': 'Emprunt non trouvé.'}, status=status.HTTP_404_NOT_FOUND)