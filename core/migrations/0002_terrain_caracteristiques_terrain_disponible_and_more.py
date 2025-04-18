# Generated by Django 5.0.1 on 2025-04-09 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='terrain',
            name='caracteristiques',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='terrain',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='terrain',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='terrains/'),
        ),
        migrations.AddField(
            model_name='terrain',
            name='prix_par_heure',
            field=models.DecimalField(decimal_places=2, default=150, max_digits=6),
            preserve_default=False,
        ),
    ]
