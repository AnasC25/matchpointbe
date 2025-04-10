from rest_framework import generics
from rest_framework.permissions import AllowAny
from core.serializers import RegisterSerializer
from core.models import CustomUser  

class RegisterViewSet(generics.CreateAPIView):
    """Vue pour l'inscription des utilisateurs."""
    queryset = CustomUser.objects.all()  # Ajout du queryset pour plus de clarté
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
