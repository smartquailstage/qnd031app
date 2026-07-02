from datetime import timedelta, date, datetime
import datetime as dt  # Para evitar colisiones si usas time
from django.utils import timezone
from django.db.models import Count
from .models import pagos, tareas, Cita, Mensaje, Profile, InformesTerapeuticos, AdministrativeProfile, Perfil_Terapeuta, Perfil_Comercial
from django.db.models import Q
from collections import defaultdict
from django.utils.timezone import localtime, is_naive, make_aware
from django.db.models import FileField, ImageField
from django.shortcuts import get_object_or_404

# =========================================================================
# PROCESADORES DE CONTEXTO CORREGIDOS
# =========================================================================

def nuevos_mensajes(request):
    """Retorna los mensajes no leídos del perfil del usuario logueado."""
    mensajes_nuevos = []
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            mensajes_nuevos = Mensaje.objects.filter(
                receptor=profile,
                leido=False
            ).order_by('-fecha_envio')[:5]
            
    return {'mensajes_no_leidos': mensajes_nuevos}


def ultima_cita(request):
    if not request.user.is_authenticated:
        return {'ultima_cita': None}

    user = request.user

    # Caso 1: Usuario paciente
    profile = Profile.objects.filter(user=user).first()
    if profile:
        return {
            'ultima_cita': Cita.objects.filter(
                profile=profile,
                pendiente=True,
                confirmada=False,
                cancelada=False
            ).order_by('fecha', 'hora').first()
        }

    # Caso 2: Usuario terapeuta
    terapeuta = Perfil_Terapeuta.objects.filter(user=user).first()
    if terapeuta:
        return {
            'ultima_cita': Cita.objects.filter(
                profile_terapeuta=terapeuta,
                pendiente=True,
                confirmada=False,
                cancelada=False
            ).order_by('fecha', 'hora').first()
        }

    # Caso 3: Usuario administrativo
    admin = AdministrativeProfile.objects.filter(user=user).first()
    if admin:
        return {
            'ultima_cita': Cita.objects.filter(
                destinatario=admin,
                pendiente=True,
                confirmada=False,
                cancelada=False
            ).order_by('fecha', 'hora').first()
        }

    # Caso 4: Usuario comercial
    comercial = Perfil_Comercial.objects.filter(user=user).first()
    if comercial:
        return {
            'ultima_cita': Cita.objects.filter(
                comercial_meddes=comercial,
                pendiente=True,
                confirmada=False,
                cancelada=False
            ).order_by('fecha', 'hora').first()
        }

    return {'ultima_cita': None}


def ultimos_videos(request):
    # Nota: Este trae los últimos videos de la plataforma global, no está filtrado por usuario.
    # Si quieres que sea del usuario actual, deberías meter un filtro por 'profile'.
    ultimos_videos = tareas.objects.filter(
        media_terapia__isnull=False,
        actividad_realizada=True
    ).exclude(media_terapia='').order_by('-fecha_actividad')[:5]

    return {'ultimos_videos_realizados': ultimos_videos}


def ultima_tarea(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            ultima_tarea = tareas.objects.filter(profile=profile).order_by('-cita_terapeutica_asignada').first()
            return {'ultima_tarea': ultima_tarea}
    return {'ultima_tarea': None}


def user_profile_data(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        return {
            'profile_photo': profile.photo.url if profile and profile.photo else None,
            'name': request.user.first_name,
            'last_name': request.user.last_name,
        }
    return {}


def mensajes_leidos_processor(request):
    mensajes_leidos = []
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            mensajes_leidos = Mensaje.objects.filter(
                receptor=profile,
                leido=True
            ).exclude(emisor__user=request.user).order_by('-fecha_envio')

    return {'mensajes_recibidos': mensajes_leidos}


def mensajes_nuevos_processor(request):
    count = 0
    mensajes = []
    conteo_por_emisor = []

    if request.user.is_authenticated:
        hoy = date.today()
        desde = hoy - timedelta(days=7)

        admin_profile = AdministrativeProfile.objects.filter(user=request.user).first()
        if admin_profile:
            mensajes_queryset = Mensaje.objects.filter(
                perfil_administrativo=admin_profile,
                leido=False,
                fecha_envio__date__gte=desde
            ).order_by('-fecha_envio')

            count = mensajes_queryset.distinct().count()
            mensajes = mensajes_queryset[:6]

            conteo_por_emisor = (
                mensajes_queryset
                .values('emisor__id', 'emisor__user__username')
                .annotate(total=Count('id', distinct=True))
                .order_by('-total')
            )

    return {
        'mensajes_nuevos': count,
        'mensajes_recientes': mensajes,
        'conteo_por_emisor': conteo_por_emisor
    }


def datos_panel_usuario(request):
    if not request.user.is_authenticated:
        return {}

    profile = Profile.objects.filter(user=request.user).first()

    # Estado de pago - Filtrado unívoco por la instancia profile
    estado_de_pago = "No disponible"
    if profile:
        try:
            ultimo_pago = pagos.objects.filter(profile=profile).latest('created_at')
            if ultimo_pago.al_dia:
                estado_de_pago = "Al día"
            elif ultimo_pago.pendiente:
                estado_de_pago = "Pendiente"
            elif ultimo_pago.vencido:
                estado_de_pago = "Vencido"
            else:
                estado_de_pago = "Sin estado"
        except pagos.DoesNotExist:
            pass

    # Conteo de mensajes, tareas y citas blindados contra duplicaciones
    cantidad_mensajes_recibidos = Mensaje.objects.filter(receptor=profile).count() if profile else 0
    cantidad_terapias_realizadas = tareas.objects.filter(profile=profile, tarea_realizada=True).distinct().count() if profile else 0
    citas_realizadas = Cita.objects.filter(profile=profile, confirmada=True).count() if profile else 0

    # Estado de la terapia
    estado_terapia = "No definido"
    if profile:
        if profile.es_en_terapia:
            estado_terapia = "En terapia"
        elif profile.es_retirado:
            estado_terapia = "Retirado"
        elif profile.es_pausa:
            estado_terapia = "En pausa"
        elif profile.es_alta:
            estado_terapia = "Alta"

    return {
        'estado_de_pago': estado_de_pago,
        'cantidad_mensajes_recibidos': cantidad_mensajes_recibidos,
        'cantidad_terapias_realizadas': cantidad_terapias_realizadas,
        'citas_realizadas': citas_realizadas,
        'estado_terapia': estado_terapia,
    }


def citas_context(request):
    """Maneja las estadísticas de citas para el contexto global."""
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            citas = Cita.objects.filter(profile=profile)
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
        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            return {}

        # Filtramos estrictamente por la instancia de perfil y agregamos distinct() preventivo
        tareas_nuevas_qs = tareas.objects.filter(
            profile=profile,
            actividad_realizada=False
        ).order_by('-fecha_envio')

        tareas_count = tareas_nuevas_qs.distinct().count()
        tareas_detalle = tareas_nuevas_qs[:5]

        base_qs = tareas.objects.filter(profile=profile, envio_tarea=True)

        return {
            'tareas_nuevas_count': tareas_count,
            'tareas_detalle': tareas_detalle,
            'actividades_nuevas': base_qs.filter(actividad_realizada=False).distinct().count(),
            'actividades_realizadas': base_qs.filter(actividad_realizada=True).distinct().count(),
            'tareas_nuevas': tareas.objects.filter(profile=profile, actividad_realizada=False).distinct().count(),
            'tareas_con_alta': tareas.objects.filter(profile=profile, actividad_realizada=True).distinct().count(),
        }
    return {}


def pagos_context(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            pagos_pendientes = pagos.objects.filter(profile=profile, pendiente=True)
            pagos_vencidos = pagos.objects.filter(profile=profile, vencido=True)

            total_pendientes = pagos_pendientes.distinct().count()
            total_vencidos = pagos_vencidos.distinct().count()

            return {
                'pagos_pendientes_notif': pagos_pendientes,
                'pagos_vencidos_notif': pagos_vencidos,
                'total_pendientes': total_pendientes,
                'total_vencidos': total_vencidos,
                'total_pagos_nuevos': total_pendientes + total_vencidos,
            }
    return {}


def get_upload_fields(profile_instance):
    upload_fields = {}

    # Archivos del modelo Profile
    for field in profile_instance._meta.get_fields():
        if isinstance(field, (FileField, ImageField)):
            value = getattr(profile_instance, field.name)
            if value and hasattr(value, 'url'):
                label = field.verbose_name or field.name.replace('_', ' ').capitalize()
                upload_fields[label] = value.url

    # Archivos relacionados (informes) optimizados mediante la precarga
    for informe in profile_instance.informes.all():
        if informe.archivo:
            upload_fields[f"🗂 {informe.titulo}"] = informe.archivo.url

    return upload_fields


def profile_uploads_context(request):
    if request.user.is_authenticated:
        # Usamos prefetch_related para evitar el problema de N+1 consultas SQL en informes
        profiles = Profile.objects.filter(user=request.user).prefetch_related('informes')
        if profiles.exists():
            uploads = get_upload_fields(profiles.first())
            if uploads:
                return {'upload_fields': uploads}
    return {}