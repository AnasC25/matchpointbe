from django.db import models
from .Club import Club, Discipline

class Terrain(models.Model):
    id = models.CharField(primary_key=True, max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    localisation = models.CharField(max_length=255)
    prix_par_heure = models.DecimalField(max_digits=6, decimal_places=2)
    caracteristiques = models.JSONField(default=list, blank=True, null=True)
    image = models.ImageField(upload_to='terrains/', null=True, blank=True)
    disponible = models.BooleanField(default=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='terrains')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='terrains')

    def __str__(self):
        return f"{self.nom} - {self.localisation}" 