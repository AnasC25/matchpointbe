from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse, HttpResponse
from core.views import RegisterViewSet, ReservationViewSet, ReservationByDateView
from core.views.OrderViewSet import OrderViewSet
from core.views.TerrainViewSet import TerrainViewSet
from core.views.EquipmentViewSet import EquipmentViewSet
from core.views.ClubViewSet import ClubViewSet
from core.views.ClubReservationViewSet import ClubReservationViewSet

def home(request):
    return HttpResponse("OK")

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'terrains', TerrainViewSet, basename='terrain')
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'clubs', ClubViewSet, basename='club')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'club-reservations', ClubReservationViewSet, basename='club-reservation')

urlpatterns = [
    path('', home, name='home'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterViewSet.as_view(), name='register'),
    path('api/reservations/by-date/', ReservationByDateView.as_view(), name='reservations-by-date'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
