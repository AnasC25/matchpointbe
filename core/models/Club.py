from django.db import models

class Club(models.Model):
    """
    Modèle représentant un club sportif.
    """
    nom = models.CharField(max_length=255, unique=True)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='clubs/', null=True, blank=True)

    def __str__(self):
        return self.nom 