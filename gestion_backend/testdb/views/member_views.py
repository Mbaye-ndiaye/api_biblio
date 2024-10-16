from ..models.member import CustomUser
from ..serializers.member_serializers import CustomUserSerializer


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
