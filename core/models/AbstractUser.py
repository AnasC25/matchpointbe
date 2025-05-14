from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from .Club import Club

# Validateur pour les numéros de téléphone marocains
phone_validator = RegexValidator(
    regex=r'^(?:(?:\+|00)212|0)[67]\d{8}$',
    message="Le numéro de téléphone doit être au format : 0612345678, 0712345678, 212612345678 ou 212712345678"
)

class CustomUserManager(BaseUserManager):
    """Gestionnaire personnalisé pour CustomUser"""

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)  # Hachage du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé étendant AbstractUser.
    
    Attributs:
        telephone (CharField): Numéro de téléphone de l'utilisateur
        niveau (CharField): Niveau sportif de l'utilisateur
        societe (CharField): Société de l'utilisateur
        club (ForeignKey): Club auquel l'utilisateur est associé
        is_club_agent (BooleanField): Indique si l'utilisateur est un agent de club
    """
    telephone = models.CharField(max_length=20, blank=True, null=True, validators=[phone_validator])
    niveau = models.CharField(max_length=50, blank=True, null=True)
    societe = models.CharField(max_length=100, blank=True, null=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='agents')
    is_club_agent = models.BooleanField(default=False)

    # Résolution du conflit avec les groupes et permissions
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="+",  # Empêche le conflit avec 'auth.User.groups'
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="+",  # Empêche le conflit avec 'auth.User.user_permissions'
        blank=True
    )

    objects = CustomUserManager()  # Utilisation du gestionnaire personnalisé

    def __str__(self):
        return self.username
