# serializers.py
from rest_framework import serializers
from core.models import Terrain, Reservation

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
    """
    Serializer pour le modèle Reservation.
    
    Ce serializer gère la conversion des données de réservation en format JSON et vice versa.
    Les champs 'user' et 'status' sont en lecture seule pour empêcher leur modification directe.
    """
    terrain = serializers.CharField()  # Définir explicitement le champ terrain

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'terrain', 'start_time', 'end_time', 'status']
        read_only_fields = ['user', 'status']  # L'utilisateur est automatiquement défini et le statut commence en 'pending'

    def validate_terrain(self, value):
        """
        Valide que le terrain existe dans la base de données.
        
        Args:
            value: ID du terrain
            
        Returns:
            Le terrain si il existe
            
        Raises:
            serializers.ValidationError: Si le terrain n'existe pas
        """
        # Nettoyer l'ID si nécessaire (retirer le nom s'il est présent)
        terrain_id = value.split(' - ')[0] if ' - ' in value else value
        
        try:
            terrain = Terrain.objects.get(id=terrain_id)
            if not terrain.disponible:
                raise serializers.ValidationError("Ce terrain n'est pas disponible pour le moment.")
            return terrain
        except Terrain.DoesNotExist:
            raise serializers.ValidationError(f"Le terrain avec l'ID '{terrain_id}' n'existe pas.")

    def validate(self, data):
        """
        Valide qu'il n'y a pas de chevauchement de réservations pour le même terrain.
        
        Args:
            data: Données de la réservation
            
        Returns:
            Les données validées
            
        Raises:
            serializers.ValidationError: Si un chevauchement est détecté
        """
        terrain = data.get('terrain')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        # Vérifier les chevauchements avec les réservations existantes
        overlapping_reservations = Reservation.objects.filter(
            terrain=terrain,
            status__in=['pending', 'confirmed'],  # Ne vérifier que les réservations actives
            start_time__lte=end_time,  # Changé de lt à lte pour inclure les chevauchements exacts
            end_time__gte=start_time   # Changé de gt à gte pour inclure les chevauchements exacts
        ).exclude(
            # Exclure les cas où la nouvelle réservation commence exactement à la fin d'une autre
            end_time=start_time
        ).exclude(
            # Exclure les cas où la nouvelle réservation se termine exactement au début d'une autre
            start_time=end_time
        )

        # Vérifier les réservations qui commencent exactement à la même heure
        same_start_time = Reservation.objects.filter(
            terrain=terrain,
            status__in=['pending', 'confirmed'],
            start_time=start_time
        )

        if overlapping_reservations.exists() or same_start_time.exists():
            raise serializers.ValidationError(
                "Ce créneau horaire est déjà réservé pour ce terrain. Veuillez choisir un autre créneau."
            )

        return data

    def create(self, validated_data):
        # Définir automatiquement l'utilisateur comme l'utilisateur connecté
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
