from ..models.emprunts_models import Emprunt
from ..models.livres_models import Livre
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..serializers.emprunts_serializers import EmpruntSerializer
from django.utils import timezone


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

        # Vérifie si le livre est disponible
        if not livre.is_available():
            return Response({'error': 'Le livre n\'est pas disponible pour l\'emprunt.'}, status=status.HTTP_400_BAD_REQUEST)

        # Si tout est bon, appelle la méthode parente pour créer l'emprunt
        return super().create(request, *args, **kwargs)

# Cheikh Gueye : Vue pour récupérer, modifier ou supprimer un emprunt spécifique
class EmpruntDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Emprunt.objects.all()
    serializer_class = EmpruntSerializer

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
