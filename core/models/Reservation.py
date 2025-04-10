# models.py
from django.db import models
from django.conf import settings
from .Terrain import Terrain  # Importer Terrain depuis son nouveau fichier

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
