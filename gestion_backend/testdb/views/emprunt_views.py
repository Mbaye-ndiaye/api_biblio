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

        emprunt.rendu = True
        emprunt.date_retour = timezone.now()
        emprunt.livre.available_copies += 1
        emprunt.livre.save()
        emprunt.save()
        
        serializer = EmpruntSerializer(emprunt)
        return Response(serializer.data)
