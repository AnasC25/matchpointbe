from django.db import models
from .Discipline import Discipline

class Club(models.Model):
    """
    Modèle représentant un club sportif.
    """
    nom = models.CharField(max_length=255, unique=True, db_index=True)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=255, db_index=True)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True, db_index=True)
    image = models.ImageField(upload_to='clubs/', null=True, blank=True)
    disciplines = models.ManyToManyField(Discipline, related_name='clubs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['nom']
        verbose_name = 'Club'
        verbose_name_plural = 'Clubs'
        indexes = [
            models.Index(fields=['ville', 'is_active']),
        ]

    def __str__(self):
        return self.nom 