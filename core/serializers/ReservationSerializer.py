# serializers.py
from rest_framework import serializers
from core.models import Terrain, Reservation
from django.utils import timezone
from datetime import datetime, timedelta

class TerrainSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Terrain.
    
    Ce serializer gère la conversion des données du modèle Terrain en format JSON et vice versa.
    Il inclut des champs personnalisés pour l'affichage des prix, des caractéristiques et des images.
    """
    price_per_hour = serializers.DecimalField(source='prix_par_heure', max_digits=6, decimal_places=2)
    features = serializers.ListField(source='caracteristiques')
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Terrain
        fields = ['id', 'nom', 'localisation', 'price_per_hour', 'features', 'img_url', 'disponible']

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


class ReservationSerializer(serializers.ModelSerializer):
    terrain = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default='pending')

    class Meta:
        model = Reservation
        fields = ['id', 'terrain', 'user', 'start_time', 'end_time', 'status']
        read_only_fields = ['user', 'status']

    def validate_terrain(self, value):
        try:
            terrain = Terrain.objects.get(id=value)
            return terrain
        except Terrain.DoesNotExist:
            raise serializers.ValidationError("Terrain non trouvé")

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        terrain = data.get('terrain')

        if start_time >= end_time:
            raise serializers.ValidationError("L'heure de fin doit être après l'heure de début")

        if start_time < timezone.now():
            raise serializers.ValidationError("Impossible de réserver dans le passé")

        if (end_time - start_time) > timedelta(hours=2):
            raise serializers.ValidationError("La réservation ne peut pas dépasser 2 heures")

        overlapping_reservations = Reservation.objects.filter(
            terrain=terrain,
            status__in=['pending', 'confirmed'],
            start_time__lte=end_time,
            end_time__gte=start_time
        )

        if overlapping_reservations.exists():
            raise serializers.ValidationError("Ce créneau est déjà réservé")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
