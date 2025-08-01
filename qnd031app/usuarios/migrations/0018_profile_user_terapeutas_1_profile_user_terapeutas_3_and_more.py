# Generated by Django 4.2.20 on 2025-07-30 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0017_mensaje_asunto_2_alter_mensaje_asunto'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_terapeutas_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='segundo_terapeuta', to='usuarios.perfil_terapeuta', verbose_name='Asignar segundo terapeuta'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_terapeutas_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tercer_terapeuta', to='usuarios.perfil_terapeuta', verbose_name='Asignar tercer terapeuta'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='destinatario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.administrativeprofile', verbose_name='Asignar cita a Administrativo'),
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user_terapeutas',
        ),
        migrations.AddField(
            model_name='profile',
            name='user_terapeutas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primer_terapeuta', to='usuarios.perfil_terapeuta', verbose_name='Asignar prmer terapeuta'),
        ),
    ]
