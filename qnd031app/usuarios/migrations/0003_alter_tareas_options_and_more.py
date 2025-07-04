# Generated by Django 4.2.20 on 2025-07-02 17:48

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_cita_destinatario'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tareas',
            options={'ordering': ['profile__user__first_name'], 'verbose_name': 'Paciente/ Tareas & Actividades Asignadas', 'verbose_name_plural': 'Tareas & Actividades Asignadas'},
        ),
        migrations.RenameField(
            model_name='tareas',
            old_name='tarea_no_realizada',
            new_name='tarea_realizada',
        ),
        migrations.RemoveField(
            model_name='tareas',
            name='realizada',
        ),
        migrations.AddField(
            model_name='tareas',
            name='asistire',
            field=models.BooleanField(default=False, verbose_name='¿Asistirá a la terapia?'),
        ),
        migrations.AddField(
            model_name='tareas',
            name='descripcion_actividad',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Describa la actividad a realizar'),
        ),
        migrations.AlterField(
            model_name='tareas',
            name='media_terapia',
            field=models.FileField(blank=True, upload_to='Videos/%Y/%m/%d/', verbose_name='Video Multimedia de actividad '),
        ),
        migrations.AlterField(
            model_name='tareas',
            name='titulo',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Título de Actividad'),
        ),
    ]
