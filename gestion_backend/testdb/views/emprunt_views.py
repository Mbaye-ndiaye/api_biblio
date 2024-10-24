from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from ..models.emprunt_model import Emprunt
from ..serializers.emprunt_serializer import EmpruntSerializer
from django.http import Http404
from rest_framework.permissions import IsAuthenticated

class EmpruntListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        emprunts = Emprunt.objects.select_related('livre', 'membre').all()
        serializer = EmpruntSerializer(emprunts, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Vérification du nombre d'emprunts en cours pour l'utilisateur
        emprunts_en_cours = Emprunt.objects.filter(membre=request.user, rendu=False).count()
        if emprunts_en_cours >= 3:
            return Response(
                {"error": "Vous avez déjà emprunté 3 livres, vous ne pouvez pas en emprunter plus pour le moment."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérification si l'utilisateur a déjà emprunté ce livre
        livre_id = request.data.get('livre')
        emprunt_existant = Emprunt.objects.filter(livre_id=livre_id, membre=request.user, rendu=False).exists()
        if emprunt_existant:
            return Response(
                {"error": "Vous avez déjà emprunté ce livre et ne l'avez pas encore rendu."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Création de l'emprunt
        serializer = EmpruntSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(membre=request.user)  # Utilisation de l'utilisateur connecté
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmpruntDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Emprunt.objects.get(pk=pk)
        except Emprunt.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        emprunt = self.get_object(pk)
        serializer = EmpruntSerializer(emprunt)
        return Response(serializer.data)

    def put(self, request, pk):
        emprunt = self.get_object(pk)

        if emprunt.rendu:
            return Response({"error": "Ce livre a déjà été rendu."}, status=status.HTTP_400_BAD_REQUEST)

        # Marquer l'emprunt comme rendu
        emprunt.rendu = True
        emprunt.date_retour = timezone.now()

        # Incrémenter le nombre de copies disponibles du livre
        emprunt.livre.available_copies += 1
        emprunt.livre.save()

        emprunt.save()

        serializer = EmpruntSerializer(emprunt)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        emprunt = self.get_object(pk)

        if emprunt.rendu is False:
            # Si l'emprunt n'est pas rendu, remettre le livre en stock avant suppression
            emprunt.livre.available_copies += 1
            emprunt.livre.save()

        emprunt.delete()
        return Response({"message": "Emprunt supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
