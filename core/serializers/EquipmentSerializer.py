from rest_framework import serializers
from core.models import Equipment      

# ✅ Serializer pour l'équipement
class EquipmentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = ['id', 'sku', 'name', 'description', 'quantity', 'available', 
                 'brand', 'category', 'price', 'prix_barre', 'discount_percentage', 
                 'stock', 'image_url', 'created_at', 'vendeur']

    def get_image_url(self, obj):
        """
        Méthode pour générer l'URL de l'image de l'équipement.
        
        Args:
            obj: Instance du modèle Equipment
            
        Returns:
            str: URL complète de l'image ou None si aucune image n'est disponible
        """
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            url = request.build_absolute_uri(obj.image.url)
            # Forcer HTTPS uniquement en production
            if not request.get_host().startswith('localhost') and not request.get_host().startswith('127.0.0.1'):
                if url.startswith('http://'):
                    url = 'https://' + url[7:]
            return url
        return None