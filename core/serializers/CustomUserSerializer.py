from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Club

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle CustomUser.
    
    Ce serializer gère la conversion des données du modèle CustomUser en format JSON et vice versa.
    """
    password = serializers.CharField(write_only=True)
    club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all(), required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 
                 'telephone', 'niveau', 'societe', 'club']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur avec les données validées.
        
        Args:
            validated_data: Données validées pour la création de l'utilisateur
            
        Returns:
            CustomUser: L'utilisateur créé
        """
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user 