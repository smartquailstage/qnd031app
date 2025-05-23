# Generated by Django 4.2.20 on 2025-04-23 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0020_perfil_terapeuta_antecedentes_penales_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsistenciaTerapeuta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora_entrada', models.TimeField()),
                ('hora_salida', models.TimeField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True)),
                ('cita_relacionada', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.cita')),
                ('terapeuta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asistencias', to='usuarios.perfil_terapeuta')),
            ],
            options={
                'ordering': ['-fecha', 'hora_entrada'],
                'unique_together': {('terapeuta', 'fecha', 'hora_entrada')},
            },
        ),
    ]
