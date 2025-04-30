from rest_framework import serializers
from core.models import Order, OrderItem
from core.serializers.EquipmentSerializer import EquipmentSerializer

# Serializer des articles d'une commande
class OrderItemSerializer(serializers.ModelSerializer):
    product = EquipmentSerializer(read_only=True)  # Afficher les détails du produit
    product_id = serializers.PrimaryKeyRelatedField(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']
        read_only_fields = ['order', 'price']


# Serializer pour les commandes
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'items', 'total_price', 'status', 'created_at']
        read_only_fields = ['user_id', 'total_price', 'status', 'created_at']


# Serializer détaillé pour les commandes avec articles
class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'items', 'total_price', 'status', 'created_at']
