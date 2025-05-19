from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from ..models.Club import Club
from ..serializers.ClubSerializer import ClubSerializer

class ClubViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les clubs. 
    Affichage public pour la liste et les détails.
    Authentification requise pour les modifications.
    """
    queryset = Club.objects.prefetch_related('disciplines').all()
    serializer_class = ClubSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'ville']
    ordering_fields = ['nom', 'ville']
    filterset_fields = ['ville', 'disciplines']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
