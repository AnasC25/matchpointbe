from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models.Club import Club
from ..serializers.ClubSerializer import ClubSerializer

class ClubViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les clubs.
    Permet de filtrer les clubs par ville.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'ville']
    ordering_fields = ['nom', 'ville']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes] 