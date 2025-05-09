from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Reservation
from datetime import datetime, time, timedelta, timezone
from django.utils import timezone as dj_timezone
import logging

logger = logging.getLogger(__name__)

class ReservationByDateView(APIView):
    """
    Vue pour récupérer la disponibilité des créneaux horaires pour une date donnée (et un terrain optionnel).
    """
    def get(self, request, date):
        try:
            # Récupérer l'ID du terrain (optionnel)
            terrain_id = request.query_params.get('terrain_id')
            logger.info(f"Requête pour la date: {date}, terrain_id: {terrain_id}")

            # Convertir la date en objet datetime
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            logger.info(f"Date convertie: {date_obj}")

            # Définir les heures d'ouverture (modifiable selon vos besoins)
            start_hour = 8
            end_hour = 24  # Pour inclure jusqu'à minuit
            slot_duration = 1  # en heures

            # Générer tous les créneaux horaires de la journée
            slots = []
            current_time = datetime.combine(date_obj, time(hour=start_hour))
            # Rendre le datetime aware dans le fuseau local
            current_time = current_time.replace(tzinfo=dj_timezone.get_current_timezone())
            logger.info(f"Heure de début: {current_time}")

            # Calculer la date de fin (jour suivant pour minuit)
            end_date = date_obj + timedelta(days=1) if end_hour == 24 else date_obj
            end_datetime = datetime.combine(end_date, time(hour=0)) if end_hour == 24 else datetime.combine(date_obj, time(hour=end_hour))
            end_datetime = end_datetime.replace(tzinfo=dj_timezone.get_current_timezone())
            logger.info(f"Heure de fin: {end_datetime}")

            while current_time < end_datetime:
                end_time = current_time + timedelta(hours=slot_duration)
                logger.debug(f"Vérification du créneau: {current_time} - {end_time}")

                # Vérifier les réservations qui recouvrent ce créneau
                reservations_qs = Reservation.objects.filter(
                    start_time__date=date_obj,  # Filtrer d'abord par date
                    start_time__hour=current_time.hour,  # Puis par heure
                    status='reserved'  # Ne vérifier que les réservations confirmées
                )
                
                if terrain_id:
                    reservations_qs = reservations_qs.filter(terrain_id=terrain_id)

                # Log pour déboguer
                logger.debug(f"Créneau {current_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}")
                logger.debug(f"Réservations trouvées: {reservations_qs.count()}")
                for res in reservations_qs:
                    logger.debug(f"Réservation: {res.start_time} - {res.end_time}")

                is_reserved = reservations_qs.exists()
                status_str = "Réservé" if is_reserved else "Disponible"

                slots.append({
                    "start": current_time.strftime('%H:%M'),
                    "end": end_time.strftime('%H:%M'),
                    "status": status_str
                })

                current_time = end_time

            logger.info(f"Nombre total de créneaux générés: {len(slots)}")
            return Response({
                "date": date,
                "slots": slots
            })

        except ValueError as ve:
            logger.error(f"Erreur de format de date: {str(ve)}")
            return Response(
                {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Erreur dans ReservationByDateView: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 