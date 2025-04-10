from django.db import models

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
    """
    id = models.CharField(primary_key=True, max_length=50, unique=True)  # ID personnalisé
    nom = models.CharField(max_length=255)
    localisation = models.CharField(max_length=255)  # correspond à la ville
    prix_par_heure = models.DecimalField(max_digits=6, decimal_places=2)
    caracteristiques = models.JSONField(default=list)  # ex: ["Éclairage", "Vestiaires"]
    image = models.ImageField(upload_to='terrains/', null=True, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.nom}" 