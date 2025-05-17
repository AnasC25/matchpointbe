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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'total_price', 'items', 'shipping_address', 'shipping_phone', 'payment_method']
        read_only_fields = ['total_price']


# Serializer détaillé pour les commandes avec articles
class OrderDetailSerializer(OrderSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_details = serializers.SerializerMethodField()

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ['shipping_details', 'payment_status', 'notes']

    def get_shipping_details(self, obj):
        return {
            'address': obj.shipping_address,
            'city': obj.shipping_city,
            'postal_code': obj.shipping_postal_code,
            'country': obj.shipping_country,
            'phone': obj.shipping_phone,
            'email': obj.shipping_email
        }
