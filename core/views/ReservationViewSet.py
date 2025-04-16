from rest_framework import viewsets, permissions
from core.models import Reservation
from core.serializers.ReservationSerializer import ReservationSerializer

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
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Un utilisateur ne peut voir que ses propres réservations
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # L'utilisateur est automatiquement défini dans le sérialiseur
        serializer.save()
