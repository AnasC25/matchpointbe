from rest_framework import viewsets, permissions
from core.models import Reservation
from core.serializers.ReservationSerializer import ReservationSerializer

class IsClubAgent(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est un agent de club.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_club_agent

class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les réservations de terrains.
    
    Ce ViewSet fournit les opérations CRUD (Create, Read, Update, Delete) pour les réservations.
    Il utilise le modèle Reservation et le serializer ReservationSerializer.
    
    Règles de permission :
    - Lecture : Authentifié = ses propres réservations uniquement
    - Création : Authentifié uniquement
    - Modification/Suppression : Agents de club uniquement
    """
    serializer_class = ReservationSerializer

    def get_permissions(self):
        """
        Définit les permissions selon l'action :
        - 'list' et 'retrieve' : Lecture uniquement pour utilisateurs authentifiés
        - 'create' : Création pour utilisateurs authentifiés
        - 'update', 'partial_update', 'destroy' : Agents de club uniquement
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsClubAgent]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Retourne uniquement les réservations de l'utilisateur connecté.
        """
        if self.request.user.is_authenticated:
            return Reservation.objects.filter(user=self.request.user)
        return Reservation.objects.none()

    def perform_create(self, serializer):
        """
        Crée une nouvelle réservation en associant l'utilisateur connecté.
        """
        serializer.save(user=self.request.user)
