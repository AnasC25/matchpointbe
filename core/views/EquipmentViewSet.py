from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Equipment
from core.serializers.EquipmentSerializer import EquipmentSerializer


# ✅ ViewSet pour l'équipement de padel avec filtres
class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # 🔹 Ajout du filtrage
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'brand', 'price', 'name']  # Filtres exacts
    search_fields = ['name', 'brand', 'category']  # Recherche partielle
    ordering_fields = ['price', 'name']  # Tri possible par prix et nom
