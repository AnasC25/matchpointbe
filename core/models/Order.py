# Importation des modules nécessaires 
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from .Equipment import Equipment  # Assurez-vous que Equipment est bien défini dans le même dossier d'application

# Modèle pour les commandes
class Order(models.Model):
    # Choix possibles pour le statut de la commande
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'En cours'), 
        ('shipped', 'Expédié'),
        ('delivered', 'Livré'),
        ('cancelled', 'Annulé')
    ]

    # Champs du modèle Order
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )  # Lien vers l'utilisateur
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création automatique
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Statut de la commande
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Prix total par défaut 0

    # Informations de livraison
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=10)
    shipping_country = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20)
    shipping_email = models.EmailField()
    
    # Informations de paiement
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Notes et commentaires
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Commande #{self.id} - {self.status}"
    
    def calculate_total_price(self):
        """ Calcule le prix total de la commande en fonction des articles. """
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_price = total
        self.save(update_fields=['total_price'])  # Met à jour uniquement le champ total_price

    class Meta:
        ordering = ['-created_at']

# Modèle pour les articles d'une commande
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")  # Ajout de related_name
    product = models.ForeignKey(Equipment, on_delete=models.CASCADE)  # Lien vers le produit
    quantity = models.IntegerField(validators=[MinValueValidator(1)])  # Quantité commandée
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} dans la commande {self.order.id}"

    def save(self, *args, **kwargs):
        """
        Vérifie la disponibilité du stock avant de sauvegarder l'OrderItem.
        Assure que le prix est bien défini avant de sauvegarder.
        """
        # Vérifier si le produit est disponible
        if not self.product.available:
            raise ValueError(f"Le produit {self.product.name} n'est plus disponible.")

        # Vérifier si le stock est suffisant
        if self.product.stock < self.quantity:
            raise ValueError(
                f"Stock insuffisant pour {self.product.name}. "
                f"Quantité demandée: {self.quantity}, Stock disponible: {self.product.stock}"
            )

        # Assure que le prix est bien défini
        if not self.price:
            self.price = self.product.price

        # Mettre à jour le stock
        self.product.stock -= self.quantity
        if self.product.stock == 0:
            self.product.available = False
        self.product.save()

        super().save(*args, **kwargs)
        self.order.calculate_total_price()  # Recalcule le prix total après chaque ajout/modification

    def get_total_price(self):
        """ Retourne le prix total de l'article """
        return self.price * self.quantity
