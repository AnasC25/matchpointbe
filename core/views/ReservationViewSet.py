from rest_framework import viewsets, permissions
from core.models import Reservation
from core.serializers.ReservationSerializer import ReservationSerializer

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre la lecture sans authentification
    mais exiger l'authentification pour la création/modification.
    """
    def has_permission(self, request, view):
        # Permettre la lecture (GET, HEAD, OPTIONS) sans authentification
        if request.method in permissions.SAFE_METHODS:
            return True
        # Exiger l'authentification pour les autres méthodes
        return request.user and request.user.is_authenticated

class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les réservations de terrains.
    
    Ce ViewSet fournit les opérations CRUD (Create, Read, Update, Delete) pour les réservations.
    Il utilise le modèle Reservation et le serializer ReservationSerializer.
    
    Attributs:
        queryset: Toutes les réservations de la base de données
        serializer_class: Le serializer utilisé pour la sérialisation/désérialisation
        permission_classes: Lecture publique, création/modification authentifiée
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Si l'utilisateur est authentifié, il ne voit que ses propres réservations
        if self.request.user.is_authenticated:
            return Reservation.objects.filter(user=self.request.user)
        # Sinon, retourner toutes les réservations
        return Reservation.objects.all()

    def perform_create(self, serializer):
        # L'utilisateur est automatiquement défini dans le sérialiseur
        serializer.save(user=self.request.user)
