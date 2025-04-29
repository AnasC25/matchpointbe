from django.db import models

class Club(models.Model):
    """
    Modèle représentant un club sportif.
    
    Attributs:
        nom (CharField): Nom du club
        adresse (CharField): Adresse du club
        ville (CharField): Ville où se trouve le club
        telephone (CharField): Numéro de téléphone du club
        email (EmailField): Adresse email du club
    """
    nom = models.CharField(max_length=255, unique=True)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nom 