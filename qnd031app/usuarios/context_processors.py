from datetime import timedelta, date
from django.db.models import Count
from .models import pagos, tareas, Cita, Mensaje, Profile
from django.db.models import Q

def mensajes_leidos_processor(request):
    if request.user.is_authenticated:
        mensajes_leidos = Mensaje.objects.filter(
            receptor=request.user,
            leido=True
        ).exclude(emisor=request.user).order_by('-fecha_envio')
    else:
        mensajes_leidos = []

    return {
        'mensajes_recibidos': mensajes_leidos
    }


def user_profile_data(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile  # o Profile.objects.get(user=request.user)
            return {
                'profile_photo': profile.photo.url if profile.photo else None,
                'name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        except:
            return {
                'profile_photo': None,
                'name': request.user.first_name,
                'last_name': request.user.last_name,
            }
    return {}


def mensajes_nuevos_processor(request):
    if request.user.is_authenticated:
        hoy = date.today()
        desde = hoy - timedelta(days=7)

        # Filtra mensajes no leídos del usuario autenticado como receptor
        mensajes_queryset = Mensaje.objects.filter(
            receptor=request.user,
            leido=False,
            fecha_envio__date__gte=desde
        ).order_by('-fecha_envio')

        count = mensajes_queryset.count()
        mensajes = mensajes_queryset[:6]

        # Agrupa por emisor y cuenta cuántos mensajes ha enviado cada uno
        conteo_por_emisor = (
            mensajes_queryset
            .values('emisor__id', 'emisor__username')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

    else:
        count = 0
        mensajes = []
        conteo_por_emisor = []

    return {
        'mensajes_nuevos': count,
        'mensajes_recientes': mensajes,
        'conteo_por_emisor': conteo_por_emisor  # Lista de diccionarios con emisor y cantidad
    }





def datos_panel_usuario(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user

    # Estado de pago
    try:
        estado = pagos.objects.get(cliente=user)
        estado_de_pago = estado.estado_de_pago
    except pagos.DoesNotExist:
        estado_de_pago = "No disponible"

    # Cantidad de mensajes
    cantidad_mensajes_recibidos = Mensaje.objects.filter(receptor=user).count()

    # Tareas realizadas
    cantidad_terapias_realizadas = tareas.objects.filter(paciente=user, realizada=True).count()

    # Citas confirmadas (ya no hay estado ni is_active/is_deleted)
    citas_realizadas = Cita.objects.filter(destinatario=user, confirmada=True).count()

    # Estado de terapia
    estado_terapia = "Activa" if cantidad_terapias_realizadas > 0 else "Pendiente"

    return {
        'estado_de_pago': estado_de_pago,
        'cantidad_mensajes_recibidos': cantidad_mensajes_recibidos,
        'cantidad_terapias_realizadas': cantidad_terapias_realizadas,
        'citas_realizadas': citas_realizadas,
        'estado_terapia': estado_terapia,
    }


def citas_context(request):
    if request.user.is_authenticated:
        # Filtrar todas las citas del destinatario
        citas = Cita.objects.filter(destinatario=request.user)

        confirmadas = citas.filter(confirmada=True).count()
        pendientes = citas.filter(pendiente=True).count()
        canceladas = citas.filter(cancelada=True).count()

        return {
            'citas_todas': citas,
            'citas_confirmadas_count': confirmadas,
            'citas_pendientes_count': pendientes,
            'citas_canceladas_count': canceladas,
        }

    return {}


def tareas_context(request):
    if request.user.is_authenticated:
        tareas_nuevas_qs = tareas.objects.filter(
            paciente=request.user,
            realizada=False
        ).order_by('-fecha_envio')

        tareas_count = tareas_nuevas_qs.count()
        tareas_detalle = tareas_nuevas_qs[:5]  # Limita si es para dropdown, o todos si lo necesitas completo

        return {
            'tareas_nuevas_count': tareas_count,
            'tareas_detalle': tareas_detalle
        }

    return {}


def pagos_context(request):
    if request.user.is_authenticated:
        pagos_pendientes = pagos.objects.filter(cliente=request.user, estado_de_pago='Pendiente')
        pagos_vencidos = pagos.objects.filter(cliente=request.user, estado_de_pago='Vencido')
        total_pagos_nuevos = pagos_pendientes.count() + pagos_vencidos.count()
        return {
            'pagos_pendientes_notif': pagos_pendientes,
            'pagos_vencidos_notif': pagos_vencidos,
            'total_pagos_nuevos': total_pagos_nuevos,
        }
    return {}