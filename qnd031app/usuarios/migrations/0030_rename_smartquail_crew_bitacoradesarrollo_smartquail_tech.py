# Generated by Django 4.2.20 on 2025-04-24 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0029_rename_smart_quail_crew_bitacoradesarrollo_smartquail_crew'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bitacoradesarrollo',
            old_name='SmartQuail_crew',
            new_name='SmartQuail_Tech',
        ),
    ]
