# Generated by Django 4.2.20 on 2025-07-29 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_alter_cliente_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='certificado_final',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='informe_inicial',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='informe_segimiento',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='informe_segimiento_2',
        ),
    ]
