# models.py
from django.db import models
from django.conf import settings
from .Terrain import Terrain  # Importer Terrain depuis son nouveau fichier
from django.utils import timezone

class Reservation(models.Model):
    """
    Modèle représentant une réservation de terrain.
    
    Attributs:
        user (ForeignKey): Utilisateur qui effectue la réservation
        terrain (ForeignKey): Terrain réservé
        start_time (DateTimeField): Date et heure de début
        end_time (DateTimeField): Date et heure de fin
        status (CharField): État de la réservation (en attente/confirmée/annulée)
    """
    STATUT_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('cancelled', 'Annulée'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    terrain = models.ForeignKey(Terrain, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUT_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.terrain.nom} ({self.start_time} - {self.end_time})"

    @classmethod
    def get_terrain_availability(cls, terrain_id, date):
        """
        Retourne la disponibilité d'un terrain pour une date donnée.
        
        Args:
            terrain_id (int): ID du terrain
            date (date): Date à vérifier
            
        Returns:
            list: Liste des créneaux horaires avec leur statut
        """
        # Heures d'ouverture (à adapter selon vos besoins)
        start_hour = 8
        end_hour = 22
        
        # Créer une liste de tous les créneaux horaires de la journée
        slots = []
        current_time = timezone.make_aware(
            timezone.datetime.combine(date, timezone.time(hour=start_hour))
        )
        
        while current_time.hour < end_hour:
            end_slot = current_time + timezone.timedelta(hours=1)
            
            # Vérifier si ce créneau est réservé
            is_reserved = cls.objects.filter(
                terrain_id=terrain_id,
                start_time__lte=current_time,
                end_time__gt=current_time,
                status__in=['pending', 'confirmed']
            ).exists()
            
            slots.append({
                'start_time': current_time,
                'end_time': end_slot,
                'is_reserved': is_reserved,
                'status': 'reserved' if is_reserved else 'available'
            })
            
            current_time = end_slot
            
        return slots
