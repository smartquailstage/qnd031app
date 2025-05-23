# Generated by Django 4.2.20 on 2025-05-22 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0068_profile_certificado_final_profile_certificado_inicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='profile_terapeuta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Asignar_perfil_de_terapeuta', to='usuarios.perfil_terapeuta', verbose_name='Asignar perfil de terapeuta'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Confirmada'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Cancelada'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Asignar_perfil_de_paciente', to='usuarios.profile', verbose_name='Asignar perfil de paciente'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='certificado_final',
            field=models.FileField(blank=True, null=True, upload_to='certificados/final/', verbose_name='Certificado de alta terapeutica'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='certificado_inicio',
            field=models.FileField(blank=True, null=True, upload_to='certificados/inicio/', verbose_name='Certificado de inicio terapeutico'),
        ),
    ]
