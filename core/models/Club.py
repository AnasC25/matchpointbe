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

    DISCIPLINE_CHOICES = [
        ('padel', 'Padel'),
        ('basket', 'Basket'),
        ('tennis', 'Tennis'),
        ('football', 'Football'),
        ('volley', 'Volley'),
        ('handball', 'Handball'),
        ('badminton', 'Badminton'),
        ('squash', 'Squash'),
        ('multisport', 'Multisport'),
    ]
    discipline = models.CharField(max_length=20, choices=DISCIPLINE_CHOICES, default='padel')

    def __str__(self):
        return self.nom 