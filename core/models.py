from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('cancelled', 'Annulé')
    ]

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    # ... autres champs ...

    def __str__(self):
        return f"Commande #{self.id} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']

class CustomUser(AbstractUser):
    # vos champs personnalisés
    telephone = models.CharField(max_length=20, blank=True)
    niveau = models.CharField(max_length=20, blank=True)
    societe = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'core_customuser'