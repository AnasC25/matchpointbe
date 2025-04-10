from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Order
from core.serializers.OrderSerializer import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commandes.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """ Retourne les commandes de l'utilisateur. """
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
        instance.status = 'processing'  # Changé de 'confirmed' à 'processing' pour correspondre aux STATUS_CHOICES
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

    @action(detail=True, methods=['post'])
    def refund(self, request, *args, **kwargs):
        # Suppression de cette méthode car 'refunded' n'est pas dans STATUS_CHOICES
        return Response({'message': 'Action non disponible'}, status=400)

    @action(detail=False, methods=['post'], url_path='create-order')
    def create_order(self, request):
        try:
            # Ajoutez automatiquement l'utilisateur aux données
            data = request.data.copy()
            data['user'] = request.user.id
            
            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Commande créée avec succès',
                    'data': serializer.data
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