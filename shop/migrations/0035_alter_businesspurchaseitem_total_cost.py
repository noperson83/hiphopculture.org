# Generated by Django 3.2.25 on 2025-01-13 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0034_remove_productsize_total_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspurchaseitem',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
