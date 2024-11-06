from ..models.member_models import Member
from ..serializers.member_serializers import MemberSerializer
from rest_framework import status
from rest_framework.response import Response
from ..serializers.auth_serializers import CustomUserSerializer
from rest_framework import generics



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
