from rest_framework import serializers
from core.models import Equipment      

# ✅ Serializer pour l'équipement
class EquipmentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = ['id', 'sku', 'name', 'description', 'available', 
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
            return request.build_absolute_uri(obj.image.url)
        return None