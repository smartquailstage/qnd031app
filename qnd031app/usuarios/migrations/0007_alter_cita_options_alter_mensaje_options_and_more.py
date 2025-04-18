# Generated by Django 4.2.20 on 2025-04-14 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0006_alter_mensaje_asunto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cita',
            options={'ordering': ['-fecha'], 'verbose_name': 'Cita', 'verbose_name_plural': 'Registro de Citas'},
        ),
        migrations.AlterModelOptions(
            name='mensaje',
            options={'ordering': ['-fecha_envio'], 'verbose_name': 'Mensaje de Paciente', 'verbose_name_plural': 'Bandeja de entrada Pacientes'},
        ),
        migrations.AlterModelOptions(
            name='perfil_terapeuta',
            options={'ordering': ['user'], 'verbose_name': 'Terapista', 'verbose_name_plural': 'Registros de Terapistas'},
        ),
        migrations.CreateModel(
            name='prospecion_administrativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad', models.CharField(blank=True, max_length=255, null=True, verbose_name='Especialidad')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Nombre de Usuario')),
            ],
            options={
                'verbose_name': 'Administrativo / prospeciónes',
                'verbose_name_plural': 'Registros Administrativo / prospeción',
                'ordering': ['user'],
            },
        ),
    ]
