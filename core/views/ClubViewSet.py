from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from ..models.Club import Club
from ..serializers.ClubSerializer import ClubSerializer

class ClubViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les clubs.
    Permet de filtrer les clubs par ville.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'ville']
    ordering_fields = ['nom', 'ville'] 