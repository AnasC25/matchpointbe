from rest_framework import viewsets, permissions
from core.models import Reservation
from core.serializers.ReservationSerializer import ReservationSerializer

class ClubReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les réservations des terrains d'un club.
    
    Ce ViewSet permet aux agents de club de :
    - Voir toutes les réservations des terrains de leur club
    - Créer de nouvelles réservations pour les terrains de leur club
    - Modifier les réservations existantes
    - Supprimer les réservations
    """
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'club'):
            return Reservation.objects.none()
        
        club_terrains = user.club.terrains.all()
        return Reservation.objects.filter(terrain__in=club_terrains)

    def perform_create(self, serializer):
        """
        Crée une nouvelle réservation en s'assurant que le terrain appartient au club de l'agent.
        """
        terrain = serializer.validated_data['terrain']
        if terrain.club != self.request.user.club:
            raise permissions.PermissionDenied("Vous ne pouvez pas créer de réservation pour ce terrain.")
        
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Met à jour une réservation en s'assurant que le terrain appartient au club de l'agent.
        """
        terrain = serializer.validated_data['terrain']
        if terrain.club != self.request.user.club:
            raise permissions.PermissionDenied("Vous ne pouvez pas modifier cette réservation.")
        
        serializer.save() 