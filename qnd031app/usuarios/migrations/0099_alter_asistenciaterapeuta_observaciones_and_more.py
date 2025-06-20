# Generated by Django 4.2.20 on 2025-06-03 13:39

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0098_alter_mensaje_cuerpo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistenciaterapeuta',
            name='observaciones',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='En caso de no asistir, explique el motivo'),
        ),
        migrations.AlterField(
            model_name='tareas',
            name='descripcion_tarea',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Comentario o actividad a realizar'),
        ),
    ]
