from rest_framework import serializers
from core.models import Order, OrderItem
from core.serializers.EquipmentSerializer import EquipmentSerializer

# Serializer des articles d'une commande
class OrderItemSerializer(serializers.ModelSerializer):
    product = EquipmentSerializer(read_only=True)  # Afficher les détails du produit

    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['order']  # On ne veut pas modifier l'association avec une commande


# Serializer pour les commandes
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'total_price', 'status', 'created_at']  


# Serializer détaillé pour les commandes avec articles
class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Inclure les articles avec détails

    class Meta:
        model = Order
        fields = '__all__'
