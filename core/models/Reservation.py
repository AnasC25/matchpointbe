# models.py
from django.db import models
from django.conf import settings
from .Terrain import Terrain
from django.utils import timezone

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('cancelled', 'Annulée'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    terrain = models.ForeignKey(Terrain, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Réservation {self.id} - {self.terrain.nom} ({self.start_time})"

    @classmethod
    def get_available_slots(cls, date_obj, terrain=None):
        start_hour = 8
        end_hour = 24
        slot_duration = 1

        slots = []
        current_time = timezone.make_aware(
            timezone.datetime.combine(date_obj, timezone.time(hour=start_hour))
        )
        end_time = timezone.make_aware(
            timezone.datetime.combine(date_obj, timezone.time(hour=end_hour))
        )

        while current_time < end_time:
            slot_end = current_time + timezone.timedelta(hours=slot_duration)
            is_available = not cls.objects.filter(
                terrain=terrain if terrain else models.F('terrain'),
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

        return slots
