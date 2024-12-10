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
    
    def validate_available_copies(self, value):
        if self.instance is not None:
            if value > self.instance.total_copies:
                raise serializers.ValidationError("Available copies cannot exceed total copies.")
        return 
    
    def get_pdf_file(self, obj):
        if obj.pdf_file:
            return self.context['request'].build_absolute_uri(obj.pdf_file.url)
        return None
