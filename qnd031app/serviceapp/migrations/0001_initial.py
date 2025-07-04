# Generated by Django 4.2.20 on 2025-06-05 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServicioTerapeutico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lugar_servicio', models.CharField(choices=[('INSTITUCIONAL', 'Institucional'), ('DOMICILIO', 'Domicilio'), ('CONSULTA', 'Consulta')], default='INSTITUCIONAL', max_length=50, verbose_name='Lugar del servicio')),
                ('servicio', models.CharField(choices=[('TERAPIA DE LENGUAJE', 'Terapia de Lenguaje'), ('ESTIMULACIÓN COGNITIVA', 'Estimulación Cognitiva'), ('PSICOLOGÍA', 'Psicología'), ('ESTIMULACIÓN TEMPRANA', 'Estimulación Temprana'), ('VALORACIÓN', 'Valoración')], max_length=255, unique=True, verbose_name='Servicio terapéutico')),
                ('costo_por_sesion', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Costo por sesión ($)')),
                ('observacion', models.TextField(blank=True, null=True, verbose_name='Observación de servicio')),
                ('activo', models.BooleanField(default=True, verbose_name='¿Servicio activo?')),
            ],
            options={
                'verbose_name': 'Servicio Terapéutico',
                'verbose_name_plural': 'Servicios Terapéuticos',
                'ordering': ['servicio'],
            },
        ),
    ]
