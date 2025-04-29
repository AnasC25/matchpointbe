from rest_framework import viewsets, permissions
from core.models import Reservation, Terrain
from core.serializers.ReservationSerializer import ReservationSerializer

class IsClubAgent(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est un agent de club.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_club_agent

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
    permission_classes = [permissions.IsAuthenticated, IsClubAgent]

    def get_queryset(self):
        """
        Retourne uniquement les réservations des terrains appartenant au club de l'agent.
        """
        # Récupérer les terrains du club de l'agent
        club_terrains = Terrain.objects.filter(club=self.request.user.club)
        
        # Retourner les réservations de ces terrains
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