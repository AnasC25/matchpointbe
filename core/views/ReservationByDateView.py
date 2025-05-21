from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
from core.models import Reservation, Terrain

class ReservationByDateView(APIView):
    def get(self, request):
        terrain_id = request.query_params.get('terrain_id')
        date_str = request.query_params.get('date')

        if not date_str:
            return Response(
                {'error': 'Le paramètre date est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not terrain_id:
            return Response(
                {'error': 'Le paramètre terrain_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Vérifier si le terrain existe
            terrain = Terrain.objects.get(id=terrain_id)
        except Terrain.DoesNotExist:
            return Response(
                {'error': f'Terrain avec l\'ID {terrain_id} non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date_obj < timezone.now().date():
                return Response(
                    {'error': 'La date ne peut pas être dans le passé'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_hour = 8
        end_hour = 23
        slot_duration = 1

        slots = []
        current_time = timezone.make_aware(
            datetime.combine(date_obj, datetime.min.time().replace(hour=start_hour))
        )
        end_time = timezone.make_aware(
            datetime.combine(date_obj, datetime.min.time().replace(hour=end_hour, minute=59))
        )

        # Récupérer toutes les réservations pour cette date et ce terrain
        existing_reservations = Reservation.objects.filter(
            terrain_id=terrain_id,
            start_time__date=date_obj,
            status__in=['pending', 'confirmed']
        ).values_list('start_time', flat=True)

        # Convertir les heures de réservation en set pour une recherche plus rapide
        reserved_hours = {dt.hour for dt in existing_reservations}

        while current_time < end_time:
            slot_end = current_time + timedelta(hours=slot_duration)
            is_available = current_time.hour not in reserved_hours

            slots.append({
                'start_time': current_time.strftime('%H:%M'),
                'end_time': slot_end.strftime('%H:%M'),
                'available': 'false' if not is_available else 'true'
            })
            current_time = slot_end

        return Response({
            'terrain_id': terrain_id,
            'date': date_str,
            'slots': slots
        }) 