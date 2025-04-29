from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings

class Equipment(models.Model):
    id = models.AutoField(primary_key=True)  # ID incrémental
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)  # SKU du produit
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    available = models.BooleanField(default=True)
    brand = models.CharField(max_length=255)  # Marque du produit
    category = models.CharField(max_length=255)  # Catégorie du produit
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Prix courant
    prix_barre = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # Prix barré (facultatif)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Pourcentage de remise
    stock = models.IntegerField()
    image_url = models.URLField(max_length=500, blank=True, null=True)  # URL de l'image du produit
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'ajout du produit
    vendeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='equipements')

    def calculate_discount(self):
        """Calcule et met à jour le pourcentage de remise si un prix barré est défini."""
        if self.prix_barre and self.prix_barre > self.price:
            return round(((self.prix_barre - self.price) / self.prix_barre) * 100, 2)
        return 0

    def save(self, *args, **kwargs):
        """Met à jour le pourcentage de remise avant de sauvegarder l'objet."""
        self.discount_percentage = self.calculate_discount()
        super().save(*args, **kwargs)

    @property
    def is_new(self):
        """Retourne True si le produit a été ajouté il y a moins de 30 jours."""
        return self.created_at >= now() - timedelta(days=30)

    def __str__(self):
        return f"{self.id} - {self.name}"
