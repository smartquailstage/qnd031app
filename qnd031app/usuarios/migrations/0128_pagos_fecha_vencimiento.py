# Generated by Django 4.2.20 on 2025-06-14 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0127_pagos_servicio_alter_valoracionterapia_servicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagos',
            name='fecha_vencimiento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
