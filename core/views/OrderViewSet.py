from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Order, OrderItem, Equipment
from core.serializers.OrderSerializer import OrderSerializer, OrderDetailSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commandes.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """ Retourne les commandes de l'utilisateur ou toutes si admin """
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        data = self.request.data
        products = data.get('products', [])

        if not products:
            raise serializers.ValidationError("La liste des produits ne peut pas être vide")

        order = serializer.save(user=self.request.user)

        for product_data in products:
            product_id = product_data.get('productId')
            quantity = product_data.get('quantity')

            if not product_id or not quantity:
                continue

            product = Equipment.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        order.calculate_total_price()

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=['get'])
    def details(self, request, *args, **kwargs):
        """ Affiche les détails de la commande. """
        instance = self.get_object()
        serializer = OrderDetailSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'cancelled'
        instance.save()
        return Response({'message': 'Commande annulée'})

    @action(detail=True, methods=['post'])
    def confirm(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'processing'
        instance.save()
        return Response({'message': 'Commande confirmée'})

    @action(detail=True, methods=['post'])
    def process(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'processing'
        instance.save()
        return Response({'message': 'Commande en cours de traitement'})

    @action(detail=True, methods=['post'])
    def ship(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'shipped'
        instance.save()
        return Response({'message': 'Commande expédiée'})

    @action(detail=True, methods=['post'])
    def deliver(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'delivered'
        instance.save()
        return Response({'message': 'Commande livrée'})

    @action(detail=False, methods=['post'], url_path='create-order')
    def create_order(self, request):
        try:
            products = request.data.get('products', [])
            if not products:
                return Response(
                    {'status': 'error', 'message': 'La liste des produits ne peut pas être vide'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            for product_data in products:
                if 'productId' not in product_data or 'quantity' not in product_data:
                    return Response(
                        {'status': 'error', 'message': 'Chaque produit doit avoir un productId et une quantity'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                product_id = product_data['productId']
                quantity = product_data['quantity']

                if quantity < 1:
                    return Response(
                        {'status': 'error', 'message': f'Quantité invalide pour le produit {product_id}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if not Equipment.objects.filter(id=product_id).exists():
                    return Response(
                        {'status': 'error', 'message': f'Produit avec ID {product_id} non trouvé'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                order = serializer.save(user=request.user)

                for product_data in products:
                    product = Equipment.objects.get(id=product_data['productId'])
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=product_data['quantity'],
                        price=product.price
                    )

                order.calculate_total_price()

                return Response({
                    'status': 'success',
                    'message': 'Commande créée avec succès',
                    'data': OrderSerializer(order).data
                }, status=status.HTTP_201_CREATED)

            return Response({
                'status': 'error',
                'message': 'Erreur de validation',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
