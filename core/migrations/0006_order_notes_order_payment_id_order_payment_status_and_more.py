# Generated by Django 5.2 on 2025-05-09 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_equipment_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(default='Non spécifié'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_city',
            field=models.CharField(default='Non spécifié', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_country',
            field=models.CharField(default='Non spécifié', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_email',
            field=models.EmailField(default='non@specifie.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_phone',
            field=models.CharField(default='0000000000', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_postal_code',
            field=models.CharField(default='00000', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('reserved', 'Réservé'), ('cancelled', 'Annulé')], default='reserved', max_length=10),
        ),
    ]
