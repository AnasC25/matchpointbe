from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_copy_discipline_to_discipline_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='terrain',
            name='discipline',
        ),
        migrations.RenameField(
            model_name='terrain',
            old_name='discipline_fk',
            new_name='discipline',
        ),
    ] 