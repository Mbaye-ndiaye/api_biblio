from rest_framework import serializers
from ..models.book import Book 


class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = '__all__'
        
    def get_cover_image(self, obj):
        if obj.cover_image:
            return self.context['request'].build_absolute_uri(obj.cover_image.url)
        return None
        
    def validate_cover_image(self, value):
        if value:
            if value.content_type not in ['image/jpeg', 'image/png']:
                raise serializers.ValidationError("Le fichier n'est pas une image valide.")
        else:
            raise serializers.ValidationError("Aucun fichier téléchargé.")
        return value
    
    def validate_available_copies(self, value):
        # Vérifiez si l'instance est définie (pour les mises à jour)
        if self.instance is not None:
            if value > self.instance.total_copies:
                raise serializers.ValidationError("Available copies cannot exceed total copies.")
        return value