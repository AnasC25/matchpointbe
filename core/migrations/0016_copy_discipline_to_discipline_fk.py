from django.db import migrations

def copy_discipline_to_discipline_fk(apps, schema_editor):
    Terrain = apps.get_model('core', 'Terrain')
    Discipline = apps.get_model('core', 'Discipline')
    for terrain in Terrain.objects.all():
        discipline = Discipline.objects.get(nom=terrain.discipline)
        terrain.discipline_fk = discipline
        terrain.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_terrain_discipline_fk_alter_terrain_discipline'),
    ]

    operations = [
        migrations.RunPython(copy_discipline_to_discipline_fk),
    ] 