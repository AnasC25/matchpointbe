from rest_framework import serializers
from core.models import Terrain, Club, Discipline

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'nom', 'description']

class ClubSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Club.
    """
    class Meta:
        model = Club
        fields = ['id', 'nom', 'adresse', 'ville', 'telephone', 'email']

class TerrainSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Terrain.
    
    Ce serializer gère la conversion des données du modèle Terrain en format JSON et vice versa.
    """
    price_per_hour = serializers.DecimalField(source='prix_par_heure', max_digits=6, decimal_places=2)
    features = serializers.ListField(source='caracteristiques')
    img_url = serializers.SerializerMethodField()
    club = ClubSerializer(read_only=True)
    discipline = DisciplineSerializer(read_only=True)
    discipline_id = serializers.PrimaryKeyRelatedField(
        queryset=Discipline.objects.all(),
        write_only=True,
        source='discipline'
    )

    class Meta:
        model = Terrain
        fields = ['id', 'nom', 'localisation', 'price_per_hour', 'features', 'img_url', 
                 'disponible', 'discipline', 'discipline_id', 'club']
        read_only_fields = []

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
