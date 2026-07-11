import os
import sys
import django

# 1. Configuración de rutas para evitar conflictos con Celery y módulos locales
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 2. Configuración del entorno de Django (Por defecto usa local, se puede cambiar en terminal)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qnd031app.settings.local')
django.setup()

# 3. Importación de modelos (Siempre después de django.setup())
from usuarios.models import Profile  

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
            # .add() se encarga de crear los registros en la tabla intermedia automáticamente
            perfil.terapeutas.add(*terapeutas_a_vincular)
            contador += 1
            print(f"✅ Terapeutas migrados para el paciente: {perfil.nombre_paciente} {perfil.apellidos_paciente}")

    print(f"\n🎉 ¡Proceso terminado con éxito! Se actualizaron {contador} perfiles.")

if __name__ == '__main__':
    migrar_datos_terapeutas()