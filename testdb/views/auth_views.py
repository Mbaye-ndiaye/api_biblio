# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from ..serializers.auth_serializers import UserRegistrationSerializer, UserLoginSerializer
# from ..serializers.auth_serializers import CustomUserSerializer
# from ..models.auth_models import CustomUser

# @api_view(['POST'])
# def register(request):
#     serializer = UserRegistrationSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'user': UserRegistrationSerializer(user).data,
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def login(request):
#     serializer = UserLoginSerializer(data=request.data)
#     if serializer.is_valid():
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']
#         user = authenticate(email=email, password=password)
        
#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'user': UserRegistrationSerializer(user).data,
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         return Response({
#             'error': 'Email ou mot de passe incorrect'
#         }, status=status.HTTP_401_UNAUTHORIZED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_users(request):
#     users = CustomUser.objects.all()  # Récupérer tous les utilisateurs inscrits
#     serializer = CustomUserSerializer(users, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     try:
#         refresh_token = request.data["refresh"]
#         token = RefreshToken(refresh_token)
#         token.blacklist()
#         return Response({
#             'message': 'Déconnexion réussie'
#         }, status=status.HTTP_200_OK)
#     except Exception:
#         return Response({
#             'error': 'Token invalide'
#         }, status=status.HTTP_400_BAD_REQUEST)
    










# views/auth_views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from ..serializers.auth_serializers import UserRegistrationSerializer, UserLoginSerializer
from ..models.auth_models import CustomUser
from ..serializers.auth_serializers import CustomUserSerializer


@api_view(['POST'])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
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
            # Vérifier si l'utilisateur a déjà un token valide
            try:
                existing_token = RefreshToken.for_user(user)
                return Response({
                    'user': UserRegistrationSerializer(user).data,
                    'access': str(existing_token.access_token),
                }, status=status.HTTP_200_OK)
            except Exception:
                # Si pas de token valide, en créer un nouveau
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserRegistrationSerializer(user).data,
                    'access': str(refresh.access_token),
                })
        return Response({
            'error': 'Email ou mot de passe incorrect'
        }, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_users(request):
    """
    Récupérer la liste de tous les utilsateurs.

    Cette API retourne tous les éléments Todo dans la base de données sous forme de liste.
    """
    users = CustomUser.objects.all()  # Récupérer tous les utilisateurs inscrits
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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