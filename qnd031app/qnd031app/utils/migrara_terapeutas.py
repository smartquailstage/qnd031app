import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qnd031app.settings.pro') # <-- Cambia 'tu_proyecto' por el nombre real de tu carpeta de configuración
django.setup()

from qnd031app.models import Profile  # <-- Cambia 'usuarios' por el nombre real de tu app

def migrar_datos_terapeutas():
    print("Iniciando la migración automática de terapeutas...")
    perfiles = Profile.objects.all()
    contador = 0

    for perfil in perfiles:
        terapeutas_a_vincular = []

        # Recolectamos los terapeutas antiguos si existen y evitamos duplicados
        if perfil.user_terapeutas and perfil.user_terapeutas not in terapeutas_a_vincular:
            terapeutas_a_vincular.append(perfil.user_terapeutas)
        if perfil.user_terapeutas_1 and perfil.user_terapeutas_1 not in terapeutas_a_vincular:
            terapeutas_a_vincular.append(perfil.user_terapeutas_1)
        if perfil.user_terapeutas_3 and perfil.user_terapeutas_3 not in terapeutas_a_vincular:
            terapeutas_a_vincular.append(perfil.user_terapeutas_3)

        # Los agregamos a la nueva relación ManyToMany
        if terapeutas_a_vincular:
            # .add() se encarga de crear los registros en 'AsignacionTerapeutaPaciente' automáticamente
            perfil.terapeutas.add(*terapeutas_a_vincular)
            contador += 1
            print(f"✅ Terapeutas migrados para el paciente: {perfil.nombre_paciente} {perfil.apellidos_paciente}")

    print(f"🎉 ¡Proceso terminado con éxito! Se actualizaron {contador} perfiles.")

if __name__ == '__main__':
    migrar_datos_terapeutas()