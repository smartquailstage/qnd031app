# Generated by Django 4.2.20 on 2025-06-03 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0095_alter_asistenciaterapeuta_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistenciaterapeuta',
            name='terapeuta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Asignar_perfil_de_terapeuta2', to='usuarios.perfil_terapeuta', verbose_name='Asignar perfil de terapeuta'),
        ),
    ]
