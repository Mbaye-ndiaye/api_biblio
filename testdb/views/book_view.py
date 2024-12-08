from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from ..serializers.book_serializer import BookSerializer
from ..models.book import Book


class BookListCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser] 

    def get(self, request, *args, **kwargs):
        """
        Récupérer la liste de tous les books.

        Cette API retourne tous les éléments Todo dans la base de données sous forme de liste.
        """
        books = Book.objects.all()  # Récupérer tous les livres
        serializer = BookSerializer(books, many=True, context={'request': request})  
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        
        serializer = BookSerializer(data=request.data, context={'request': request})  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class BookDetailView(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    # Récupérer un livre spécifique (GET /books/{id}/)
    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    # Mettre à jour un livre (PUT /books/{id}/)
    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Supprimer un livre (DELETE /books/{id}/)
    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
