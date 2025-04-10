from rest_framework import viewsets, permissions
from core.models import Terrain
from core.serializers.TerrainSerializer import TerrainSerializer

class TerrainViewSet(viewsets.ModelViewSet):
    queryset = Terrain.objects.all()
    serializer_class = TerrainSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]  # Seuls les admins
        return [permissions.IsAuthenticatedOrReadOnly()]  # Lecture possible sans être admin
