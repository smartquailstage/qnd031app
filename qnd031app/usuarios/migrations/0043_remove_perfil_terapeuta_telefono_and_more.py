# Generated by Django 4.2.20 on 2025-05-13 13:54

import django.core.validators
from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0042_alter_perfil_terapeuta_datos_bancarios_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil_terapeuta',
            name='telefono',
        ),
        migrations.AddField(
            model_name='perfil_terapeuta',
            name='telefonos_contacto',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+593', max_length=128, region=None, validators=[django.core.validators.RegexValidator(message='El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX.', regex='^\\+?593?\\d{9,15}$')], verbose_name='Teléfono de persona a cargo'),
        ),
    ]
