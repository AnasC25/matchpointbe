from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Reservation
from datetime import datetime, time, timedelta
from django.utils import timezone
import pytz
from django.utils.timezone import utc

class ReservationByDateView(APIView):
    """
    Vue pour récupérer la disponibilité des créneaux horaires pour une date donnée (et un terrain optionnel).
    """
    def get(self, request, date):
        try:
            # Récupérer l'ID du terrain (optionnel)
            terrain_id = request.query_params.get('terrain_id')
            # Convertir la date en objet datetime
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()

            # Définir les heures d'ouverture (modifiable selon vos besoins)
            start_hour = 8
            end_hour = 22
            slot_duration = 1  # en heures

            # Générer tous les créneaux horaires de la journée
            slots = []
            current_time = datetime.combine(date_obj, time(hour=start_hour))
            # Correction zoneinfo : rendre le datetime aware
            current_time = current_time.replace(tzinfo=timezone.get_current_timezone())

            while current_time.hour < end_hour:
                end_time = current_time + timedelta(hours=slot_duration)

                # Convertir en UTC pour la comparaison
                current_time_utc = current_time.astimezone(timezone.utc)
                end_time_utc = end_time.astimezone(timezone.utc)

                # Filtrer les réservations qui recouvrent ce créneau
                reservations_qs = Reservation.objects.filter(
                    start_time__lt=end_time_utc,
                    end_time__gt=current_time_utc,
                    status='confirmed',
                    terrain_id=terrain_id
                )

                is_reserved = reservations_qs.exists()
                status_str = "Indisponible" if is_reserved else "Disponible"

                slots.append({
                    "start": current_time.strftime('%H:%M'),
                    "end": end_time.strftime('%H:%M'),
                    "status": status_str
                })

                current_time = end_time

            return Response({
                "date": date,
                "slots": slots
            })

        except ValueError:
            return Response(
                {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 