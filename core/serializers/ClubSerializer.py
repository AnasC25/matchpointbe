from rest_framework import serializers
from ..models.Club import Club, Discipline

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'nom', 'description']

class ClubSerializer(serializers.ModelSerializer):
    disciplines = DisciplineSerializer(many=True, read_only=True)
    disciplines_ids = serializers.PrimaryKeyRelatedField(
        queryset=Discipline.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='disciplines'
    )

    class Meta:
        model = Club
        fields = ['id', 'nom', 'adresse', 'ville', 'telephone', 'email', 'image', 'disciplines', 'disciplines_ids'] 