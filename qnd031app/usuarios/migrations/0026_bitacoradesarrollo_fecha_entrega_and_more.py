# Generated by Django 4.2.20 on 2025-04-24 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0025_bitacoradesarrollo'),
    ]

    operations = [
        migrations.AddField(
            model_name='bitacoradesarrollo',
            name='fecha_entrega',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bitacoradesarrollo',
            name='incarge',
            field=models.CharField(blank=True, choices=[('DeV', 'Mauricio Silva'), ('Prod', 'Andres Espinoza'), ('Front', 'Virginia Lasta')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bitacoradesarrollo',
            name='tipo_cambio',
            field=models.CharField(choices=[('RAPP', 'Registro administrativo/Perfil de Paciente'), ('RAPT', 'Registro administrativo/Perfil de Terapistas'), ('RAACC', 'Registro administrativo/Agenda de Citas Regulares'), ('RAPA', 'Registro administrativo/Prospeción Administrativa'), ('RAPS', 'Registro administrativo/Pago de Servicios'), ('RTTA', 'Registro Terapeutico/Tareas & Actividades'), ('RTAA', 'Registro Terapeutico/Asistencias'), ('SBN ', 'Bandeja de Notificaciones'), ('SERP', 'Visualización de ERP ')], max_length=200),
        ),
        migrations.AlterField(
            model_name='bitacoradesarrollo',
            name='tipo_tecnologia',
            field=models.CharField(choices=[('UX', 'Experiencia de Usuario'), ('UI', 'Interfase'), ('I+D', 'Implementación'), ('A', 'Automatización')], max_length=200),
        ),
        migrations.AlterField(
            model_name='bitacoradesarrollo',
            name='version_relacionada',
            field=models.CharField(blank=True, choices=[('QND0301', 'QND-0.3.0.1'), ('QND0302', 'QND-0.3.0.2'), ('QND0303', 'QND-0.3.0.3'), ('QND0304', 'QND-0.3.0.4')], max_length=200, null=True),
        ),
    ]
