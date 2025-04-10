from rest_framework import serializers
from core.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'telephone', 'niveau', 'societe', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Utilisation de create_user pour assurer le hachage du mot de passe."""
        return CustomUser.objects.create_user(**validated_data)
