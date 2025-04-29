from django.db import models
from .Club import Club

class Terrain(models.Model):
    """
    Modèle représentant un terrain de sport.
    
    Attributs:
        id (CharField): Identifiant personnalisé du terrain
        nom (CharField): Nom du terrain
        localisation (CharField): Ville où se trouve le terrain
        prix_par_heure (DecimalField): Tarif horaire de location
        caracteristiques (JSONField): Liste des équipements disponibles
        image (ImageField): Photo du terrain (optionnelle)
        disponible (BooleanField): Indique si le terrain est actuellement disponible
        discipline (CharField): Type de sport pratiqué sur le terrain
        club (ForeignKey): Club auquel appartient le terrain
    """
    DISCIPLINE_CHOICES = [
        ('FOOTBALL_11', 'Football 11 vs 11'),
        ('FOOTBALL_5', 'Football 5 vs 5'),
        ('FOOTBALL_6', 'Football 6 vs 6'),
        ('PADEL_2', 'Padel 2 vs 2'),
        ('BASKET_3', 'Basket 3 vs 3'),
    ]

    id = models.CharField(primary_key=True, max_length=50, unique=True)  # ID personnalisé
    nom = models.CharField(max_length=255)
    localisation = models.CharField(max_length=255)  # correspond à la ville
    prix_par_heure = models.DecimalField(max_digits=6, decimal_places=2)
    caracteristiques = models.JSONField(default=list, blank=True, null=True)  # ex: ["Éclairage", "Vestiaires"]
    image = models.ImageField(upload_to='terrains/', null=True, blank=True)
    disponible = models.BooleanField(default=True)
    discipline = models.CharField(max_length=20, choices=DISCIPLINE_CHOICES, default='FOOTBALL_11')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='terrains')

    def __str__(self):
        return f"{self.nom} ({self.club.nom})" 