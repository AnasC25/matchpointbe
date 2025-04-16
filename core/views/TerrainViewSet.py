from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from core.models import Terrain
from core.serializers.TerrainSerializer import TerrainSerializer

class TerrainFilter(FilterSet):
    city = CharFilter(field_name='localisation', lookup_expr='icontains')
    discipline = CharFilter(field_name='discipline')

    class Meta:
        model = Terrain
        fields = ['localisation', 'discipline']

class TerrainViewSet(viewsets.ModelViewSet):
    queryset = Terrain.objects.all()
    serializer_class = TerrainSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['id', 'nom', 'localisation', 'caracteristiques', 'discipline']
    filterset_class = TerrainFilter

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]  # Seuls les admins
        return [permissions.IsAuthenticatedOrReadOnly()]  # Lecture possible sans être admin
