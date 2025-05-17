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

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_hour = 8
        end_hour = 24
        slot_duration = 1

        slots = []
        current_time = timezone.make_aware(
            datetime.combine(date_obj, datetime.min.time().replace(hour=start_hour))
        )
        end_time = timezone.make_aware(
            datetime.combine(date_obj, datetime.min.time().replace(hour=end_hour))
        )

        while current_time < end_time:
            slot_end = current_time + timedelta(hours=slot_duration)
            is_available = not Reservation.objects.filter(
                terrain_id=terrain_id if terrain_id else models.F('terrain_id'),
                start_time__date=date_obj,
                start_time__hour=current_time.hour,
                status='reserved'
            ).exists()

            slots.append({
                'start_time': current_time,
                'end_time': slot_end,
                'available': is_available
            })
            current_time = slot_end

        return Response(slots) 