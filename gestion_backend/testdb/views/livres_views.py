from ..models.livres import Livre
from ..serializers.livres_serializers import LivreSerializer

# Cheikh Gueye : Vue pour la liste et création des livres
class LivreListCreateView(generics.ListCreateAPIView):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer

class LivreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer