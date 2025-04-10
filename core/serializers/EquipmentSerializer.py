from rest_framework import serializers
from core.models import Equipment      

# ✅ Serializer pour l'équipement
class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'