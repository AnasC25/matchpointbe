from django.db import models

class Discipline(models.Model):
    """
    Modèle représentant une discipline sportive.
    """
    nom = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nom

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
    disciplines = models.ManyToManyField(Discipline, related_name='clubs')

    def __str__(self):
        return self.nom 