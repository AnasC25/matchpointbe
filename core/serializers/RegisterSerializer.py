from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import re

CustomUser = get_user_model()  # Utiliser le modèle défini dans AUTH_USER_MODEL

class RegisterSerializer(serializers.ModelSerializer):
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
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'first_name', 
                 'last_name', 'telephone')

    def validate_telephone(self, value):
        digits = re.sub(r'\D', '', value)
        # Cas 0612345678 ou 0712345678
        if len(digits) == 10 and digits.startswith(('06', '07')):
            return '+212' + digits[1:]
        # Cas 212612345678 ou 212712345678
        if len(digits) == 12 and (digits.startswith('2126') or digits.startswith('2127')):
            return '+' + digits
        raise serializers.ValidationError(
            "Le numéro doit être au format valide (ex: 0612345678, 0712345678, 212612345678, 212712345678)."
        )

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
