from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Reservation
from core.serializers import ReservationSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les réservations de terrains.
    
    Ce ViewSet fournit les opérations CRUD (Create, Read, Update, Delete) pour les réservations.
    Il utilise le modèle Reservation et le serializer ReservationSerializer.
    
    Attributs:
        queryset: Toutes les réservations de la base de données
        serializer_class: Le serializer utilisé pour la sérialisation/désérialisation
        permission_classes: Seuls les utilisateurs authentifiés peuvent accéder à ces endpoints
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
