from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import re

CustomUser = get_user_model()  # Utiliser le modèle défini dans AUTH_USER_MODEL

class RegisterSerializer(serializers.ModelSerializer):
    NIVEAU_CHOICES = [
        ('Debutant', 'Débutant'),
        ('Intermediaire', 'Intermédiaire'),
        ('Avance', 'Avancé')
    ]

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    telephone = serializers.CharField(required=True)
    niveau = serializers.ChoiceField(choices=NIVEAU_CHOICES, required=True)
    societe = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'first_name', 
                 'last_name', 'telephone', 'niveau', 'societe')

    def validate_telephone(self, value):
        pattern = r'^6[0-9]{8}$'  # Numéro marocain valide : commence par 6 et contient 9 chiffres au total
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Le numéro doit être au format valide (ex: 612345678)."
            )
        return f"+212{value[-9:]}"  # On garde uniquement les 9 derniers chiffres et on ajoute +212

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)  # Retirer le champ password2 qui n'est pas dans le modèle
        password = validated_data.pop('password')

        # Créer l'utilisateur en utilisant create_user (qui gère le hachage du mot de passe)
        user = CustomUser.objects.create_user(password=password, **validated_data)

        return user
