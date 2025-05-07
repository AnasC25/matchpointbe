from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from datetime import datetime
from django.utils import timezone

class TerrainAvailabilityView(APIView):
    def get(self, request, terrain_id):
        """
        Retourne la disponibilité d'un terrain pour une date donnée.
        
        Paramètres:
            terrain_id (int): ID du terrain
            date (str, optionnel): Date au format YYYY-MM-DD (par défaut: aujourd'hui)
        """
        try:
            # Récupérer la date depuis les paramètres de requête
            date_str = request.query_params.get('date')
            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                date = timezone.now().date()
            
            # Obtenir les créneaux horaires
            slots = Reservation.get_terrain_availability(terrain_id, date)
            
            # Formater la réponse
            formatted_slots = []
            for slot in slots:
                formatted_slots.append({
                    'start_time': slot['start_time'].strftime('%H:%M'),
                    'end_time': slot['end_time'].strftime('%H:%M'),
                    'is_reserved': slot['is_reserved'],
                    'status': slot['status']
                })
            
            return Response({
                'date': date.strftime('%Y-%m-%d'),
                'slots': formatted_slots
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

class ReservationByDateView(APIView):
    """
    Vue pour récupérer toutes les réservations confirmées pour une date donnée.
    """
    def get(self, request, date):
        try:
            # Convertir la date en objet datetime
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Récupérer toutes les réservations confirmées pour cette date
            reservations = Reservation.objects.filter(
                start_time__date=date_obj,
                status='confirmed'
            ).select_related('terrain')
            
            # Formater la réponse
            formatted_reservations = []
            for reservation in reservations:
                formatted_reservations.append({
                    'id': reservation.id,
                    'terrain': reservation.terrain.id,
                    'start_time': reservation.start_time.isoformat(),
                    'end_time': reservation.end_time.isoformat(),
                    'status': reservation.status
                })
            
            return Response(formatted_reservations)
            
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