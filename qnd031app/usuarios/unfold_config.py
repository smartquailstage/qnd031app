from django.utils.timezone import now
from usuarios.models import Perfil_Terapeuta
from usuarios.models import prospecion_administrativa
from usuarios.models import Profile
from usuarios.models import Cita, pagos
from usuarios.models import ValoracionTerapia
from usuarios.models import tareas
from usuarios.models import AsistenciaTerapeuta
from django.utils import timezone
from usuarios.models import Mensaje
from usuarios.models import Prospeccion

def badge_callback_meddes(request):
    try:
        total = Prospeccion.objects.count()
        return f"{total}"
    except Exception:
        return "0"

def badge_callback_notificaciones(request):
    try:
        hoy = timezone.now().date()
        mensajes_hoy = Mensaje.objects.filter(creado__date=hoy).count()

        return f"{mensajes_hoy}"

    except Exception:
        return "0"


def badge_callback_asistencias(request):
    try:
        asistencias = {
            "Confirmaron asistencia": AsistenciaTerapeuta.objects.filter(asistire=True).count(),
            "No asistirán": AsistenciaTerapeuta.objects.filter(no_asistire=True).count(),
        }

        return " | ".join(f"{value}" for key, value in asistencias.items())

    except Exception:
        return "0"


def badge_callback_tareas(request):
    try:
        tareas = {
            "Realizadas": tareas.objects.filter(realizada=True).count(),
            "Pendientes": tareas.objects.filter(tarea_no_realizada=True).count(),
        }

        return " | ".join(f"{key}: {value}" for key, value in tareas.items())

    except Exception:
        return "0"


def badge_callback_valoracion(request):
    try:
        valoraciones = {
            "Particular": ValoracionTerapia.objects.filter(es_particular=True).count(),
            "Convenio": ValoracionTerapia.objects.filter(es_convenio=True).count(),
        }

        return " | ".join(f"{value}" for key, value in valoraciones.items())

    except Exception:
        return "0"



def badge_callback_pagos(request):
    try:
        pagos_estado = {
            "pendientes": pagos.objects.filter(pendiente=True).count(),
            "al_dia": pagos.objects.filter(al_dia=True).count(),
            "vencidos": pagos.objects.filter(vencido=True).count(),
        }

        return " | ".join(str(value) for value in pagos_estado.values())

    except Exception:
        return "0"



def badge_callback_citas(request):
    try:
        citas = {
            "pendientes": Cita.objects.filter(pendiente=True).count(),
            "confirmadas": Cita.objects.filter(confirmada=True).count(),
            "canceladas": Cita.objects.filter(cancelada=True).count(),
        }

        return " | ".join(str(value) for value in citas.values())

    except Exception:
        return "0"


def badge_callback_terapeutico(request):
        try:
            estados = {
                "En Terapia": Profile.objects.filter(es_en_terapia=True).count(),
            # "Retirado": Profile.objects.filter(es_retirado=True).count(),
                "Alta": Profile.objects.filter(es_alta=True).count(),
                "Pausa": Profile.objects.filter(es_pausa=True).count(),
            }

            return " | ".join(f"{value}" for key, value in estados.items())

        except Exception:
            return "0"


def badge_callback_prospeccion(request):
    try:
        estados = {
           # "PC": prospecion_administrativa.objects.filter(es_por_contactar=True).count(),
            "CT": prospecion_administrativa.objects.filter(es_contactado=True).count(),
           # "CIT": prospecion_administrativa.objects.filter(es_en_cita=True).count(),
          #  "CNV": prospecion_administrativa.objects.filter(es_convenio_firmado=True).count(),
          #  "CAP": prospecion_administrativa.objects.filter(es_capacitacion=True).count(),
           # "VAL": prospecion_administrativa.objects.filter(es_valoracion=True).count(),
           # "TER": prospecion_administrativa.objects.filter(es_en_terapia=True).count(),
          #  "REJ": prospecion_administrativa.objects.filter(es_rechazado=True).count(),
            "FIN": prospecion_administrativa.objects.filter(es_finalizado=True).count(),
           # "INA": prospecion_administrativa.objects.filter(es_inactivo=True).count(),
        }

        # Formato visual compacto
        return " | ".join(f"{value}" for key, value in estados.items())

    except Exception:
        return "0"


        

def badge_color_callback(request):
    try:
        count = Perfil_Terapeuta.objects.filter(activo=True).count()
        if count == 0:
            return "custom-green-success"
        elif count < 2:
            return "custom-green-success"
        else:
            return "custom-green-success"
    except:
        return "custom-green-success"

def badge_callback(request):
    activos = Perfil_Terapeuta.objects.filter(activo=True).count()
    inactivos = Perfil_Terapeuta.objects.filter(activo=False).count()
    return f"{activos} | {inactivos}"



def dashboard_callback(request, context):
    context.update({
        "sample": "example"
    })
    return context


def environment_callback(request):
    return ["Producción", "danger"]