from django.db import models

class Discipline(models.Model):
    """
    Modèle représentant une discipline sportive.
    """
    nom = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nom']
        verbose_name = 'Discipline'
        verbose_name_plural = 'Disciplines'

    def __str__(self):
        return self.nom 