# Generated by Django 5.0.1 on 2024-02-08 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0005_remove_purchase_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stock_app.product'),
        ),
    ]
