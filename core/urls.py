from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse
from core.views import RegisterViewSet, ReservationViewSet     # On importe uniquement les vues qui existent
from core.views import EquipmentViewSet
from core.views.OrderViewSet import OrderViewSet  # Importez la classe, pas le module
from core.views.TerrainViewSet import TerrainViewSet  # Import du TerrainViewSet

# ✅ Fonction pour la page d'accueil
def home_view(request):
    return JsonResponse({"message": "Bienvenue sur l'API MatchPoint !"})

# ✅ Création du routeur pour les ViewSets (DRF)
router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet, basename="equipment")
router.register(r'reservations', ReservationViewSet, basename="reservations")
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'terrains', TerrainViewSet, basename='terrain')

# ✅ Définition des URLs
urlpatterns = [
    # 🌍 Page d'accueil
    path('', home_view, name="home"), 
    
    # 🔹 Authentification (JWT)
    path('api/auth/register/', RegisterViewSet.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🔹 Endpoints API (ViewSets)
    path('api/', include(router.urls)),
]

# ✅ Servir les fichiers médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
