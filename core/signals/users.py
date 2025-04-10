from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """ Exécute des actions après la création d'un utilisateur. """
    if created:
        print(f"Utilisateur {instance.username} créé avec succès !")

@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, **kwargs):
    """ Exécute des actions après la mise à jour d'un utilisateur. """
    print(f"Profil utilisateur {instance.username} mis à jour.")
