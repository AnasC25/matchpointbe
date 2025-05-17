from rest_framework import serializers
from .models.Club import Club

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'nom', 'adresse', 'ville', 'telephone', 'email', 'image'] 