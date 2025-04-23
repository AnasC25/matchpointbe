from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True, null=True)
    niveau = models.CharField(max_length=50, blank=True, null=True)
    societe = models.CharField(max_length=100, blank=True, null=True)
