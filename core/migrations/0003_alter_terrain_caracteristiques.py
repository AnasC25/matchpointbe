# Generated by Django 5.0.1 on 2025-04-29 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20250428_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terrain',
            name='caracteristiques',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
