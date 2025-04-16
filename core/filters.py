import django_filters
from .models import Terrain

class TerrainFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(lookup_expr='icontains')
    localisation = django_filters.CharFilter(lookup_expr='icontains')
    prix_par_heure__lte = django_filters.NumberFilter(field_name='prix_par_heure', lookup_expr='lte')
    prix_par_heure__gte = django_filters.NumberFilter(field_name='prix_par_heure', lookup_expr='gte')
    disponible = django_filters.BooleanFilter()
    discipline = django_filters.ChoiceFilter(choices=Terrain.DISCIPLINE_CHOICES)

    class Meta:
        model = Terrain
        fields = ['nom', 'localisation', 'prix_par_heure', 'disponible', 'discipline'] 