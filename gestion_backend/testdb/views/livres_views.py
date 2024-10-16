from ..models.livres_models import Livre
from ..serializers.livres_serializers import LivreSerializer
from rest_framework import generics

# Cheikh Gueye : Vue pour la liste et création des livres
class LivreListCreateView(generics.ListCreateAPIView):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer

class LivreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer