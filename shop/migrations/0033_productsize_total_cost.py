# Generated by Django 3.2.25 on 2025-01-12 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0032_alter_businesspurchaseitem_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsize',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
