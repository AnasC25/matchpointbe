# Generated by Django 5.0.1 on 2025-04-10 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_order_sku'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
    ]
