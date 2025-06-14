from datetime import timedelta, date
from django.utils import timezone
from django.db.models import Count
from .models import pagos, tareas, Cita, Mensaje, Profile
from django.db.models import Q
from collections import defaultdict
from datetime import datetime
from django.utils.timezone import localtime, is_naive, make_aware
from django.db.models import FileField, ImageField

def citas_context(request):
    if request.user.is_authenticated:
        citas = Cita.objects.filter(destinatario=request.user).select_related('creador', 'destinatario').order_by('-fecha')[:20]

        agenda = defaultdict(lambda: defaultdict(list))
        fechas_unicas = set()
        horas_unicas = set()

        for cita in citas:
            if not cita.fecha:
                continue

            fecha = cita.fecha
            if is_naive(fecha):
                fecha = make_aware(fecha)

            fecha_local = localtime(fecha)
            dia_str = fecha_local.strftime("%Y-%m-%d")
            hora = fecha_local.strftime("%H:00")

            if fecha_local.weekday() >= 5:
                continue

            if not (9 <= fecha_local.hour <= 22):
                continue

            creador = cita.creador
            destinatario = cita.destinatario

            creador_nombre = (
                creador.get_full_name() if creador and hasattr(creador, 'get_full_name')
                else getattr(creador, 'username', 'Sin creador')
            )

            destinatario_nombre = (
                destinatario.get_full_name() if destinatario and hasattr(destinatario, 'get_full_name')
                else getattr(destinatario, 'username', 'Sin destinatario')
            )

            agenda[dia_str][hora].append({
                "id": cita.id,
                "motivo": cita.motivo or "Sin motivo",
                "creador": creador_nombre,
                "destinatario": destinatario_nombre,
                "estado": cita.estado,  # usa la propiedad
                "tipo_cita": cita.get_tipo_cita_display() if cita.tipo_cita else "Sin tipo"
            })

            fechas_unicas.add(dia_str)
            horas_unicas.add(hora)

        dias_date = [datetime.strptime(d, "%Y-%m-%d").date() for d in fechas_unicas]

        return {
            'agenda': agenda,
            'dias': sorted(dias_date),
            'horas': sorted(horas_unicas),
            'dias_str_map': {datetime.strptime(d, "%Y-%m-%d").date(): d for d in fechas_unicas}
        }

    return {}




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

    # Estado de pago (evaluar el último pago del usuario)
    try:
        ultimo_pago = pagos.objects.filter(profile__user=user).latest('created_at')
        if ultimo_pago.al_dia:
            estado_de_pago = "Al día"
        elif ultimo_pago.pendiente:
            estado_de_pago = "Pendiente"
        elif ultimo_pago.vencido:
            estado_de_pago = "Vencido"
        else:
            estado_de_pago = "Sin estado"
    except pagos.DoesNotExist:
        estado_de_pago = "No disponible"

    # Cantidad de mensajes recibidos
    cantidad_mensajes_recibidos = Mensaje.objects.filter(receptor=user).count()

    # Tareas realizadas por el paciente
    cantidad_terapias_realizadas = tareas.objects.filter(profile__user=user, realizada=True).count()

    # Citas confirmadas para el usuario
    citas_realizadas = Cita.objects.filter(destinatario=user, confirmada=True).count()

    # Estado general de terapia
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
        # Citas donde el usuario es destinatario
        citas = Cita.objects.filter(destinatario=request.user)

        return {
            'citas_todas': citas,
            'citas_confirmadas_count': citas.filter(confirmada=True).count(),
            'citas_pendientes_count': citas.filter(pendiente=True, confirmada=False, cancelada=False).count(),
            'citas_canceladas_count': citas.filter(cancelada=True).count(),
            'proximas_citas': citas.filter(fecha__gte=timezone.now()).order_by('fecha')[:5]
        }

    return {}


def tareas_context(request):
    if request.user.is_authenticated:
        tareas_nuevas_qs = tareas.objects.filter(
            profile__user=request.user,
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
        pagos_pendientes = pagos.objects.filter(profile__user=request.user, pendiente=True)
        pagos_vencidos = pagos.objects.filter(profile__user=request.user, vencido=True)

        total_pendientes = pagos_pendientes.count()
        total_vencidos = pagos_vencidos.count()
        total_pagos_nuevos = total_pendientes + total_vencidos

        return {
            'pagos_pendientes_notif': pagos_pendientes,
            'pagos_vencidos_notif': pagos_vencidos,
            'total_pendientes': total_pendientes,
            'total_vencidos': total_vencidos,
            'total_pagos_nuevos': total_pagos_nuevos,
        }
    return {}




def get_upload_fields(profile_instance):
    upload_fields = {}
    for field in profile_instance._meta.get_fields():
        if isinstance(field, (FileField, ImageField)):
            value = getattr(profile_instance, field.name)
            if value and hasattr(value, 'url'):  # Asegura que tiene un archivo subido
                upload_fields[field.verbose_name or field.name] = value.url
    return upload_fields

def profile_uploads_context(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            uploads = get_upload_fields(profile)
            if uploads:  # Solo devolver si hay archivos subidos
                return {
                    'upload_fields': uploads
                }
            return {}  # No mostrar nada si no hay archivos
        except Profile.DoesNotExist:
            return {}
    return {}