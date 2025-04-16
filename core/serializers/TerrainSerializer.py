from rest_framework import serializers
from core.models import Terrain

class TerrainSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Terrain.
    
    Ce serializer gère la conversion des données du modèle Terrain en format JSON et vice versa.
    """
    price_per_hour = serializers.DecimalField(source='prix_par_heure', max_digits=6, decimal_places=2)
    features = serializers.ListField(source='caracteristiques')
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Terrain
        fields = ['id', 'nom', 'localisation', 'price_per_hour', 'features', 'img_url', 'disponible', 'discipline']
        read_only_fields = []  # Aucun champ en lecture seule pour permettre la modification de l'ID

    def get_img_url(self, obj):
        """
        Méthode pour générer l'URL complète de l'image du terrain.
        
        Args:
            obj: Instance du modèle Terrain
            
        Returns:
            str: URL complète de l'image ou None si aucune image n'est disponible
        """
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None
