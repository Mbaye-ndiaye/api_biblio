from rest_framework import serializers
from ..models.book import Book 


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_available_copies(self, value):
        # Vérifiez si l'instance est définie (pour les mises à jour)
        if self.instance is not None:
            if value > self.instance.total_copies:
                raise serializers.ValidationError("Available copies cannot exceed total copies.")
        return value