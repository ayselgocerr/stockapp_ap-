# Generated by Django 5.0.1 on 2024-02-08 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0006_purchase_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='price_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
