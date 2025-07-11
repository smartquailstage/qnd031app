# usuarios/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mensaje,ValoracionTerapia
from .tasks import enviar_correo_async, enviar_whatsapp_async, enviar_correo_valoracion_async
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Mensaje)
def manejar_mensaje(sender, instance, created, **kwargs):
    if not created:
        return

    receptor = instance.receptor
    telefono = str(receptor.profile.celular)  
    telefono_meddes = str(receptor.profile.celular)  
    cuerpo = instance.cuerpo
    asunto = instance.asunto

    if asunto == "Solicitud de pago vencido":
        enviar_correo_async.delay(instance.emisor.username, receptor.email, asunto, cuerpo)
        enviar_whatsapp_async.delay(telefono, f"⚠️ Solicitud de pago pendiente:\n{cuerpo}")

    elif asunto == "Consulta":
        enviar_whatsapp_async.delay(telefono_meddes, f"📢 Mensaje informativo:\n{cuerpo}")
    
    elif asunto == "Informativo":
        enviar_whatsapp_async.delay(telefono, f"📢 Mensaje informativo:\n{cuerpo}")



@receiver(post_save, sender=ValoracionTerapia)
def notificar_valoracion(sender, instance, created, **kwargs):
    if not created:
        return

    institucion = instance.institucion
    correo_destino = institucion.mail_institucion_general if institucion else None

    if not correo_destino:
        return  # No enviar correo si la institución no tiene un email

    asunto = f"Nueva Valoración Terapéutica - {instance.nombre}"

    archivo_link = ""
    if instance.archivo_adjunto:
        archivo_url = instance.archivo_adjunto.url
        archivo_link = f"{settings.SITE_DOMAIN}{archivo_url}"

    cuerpo = f"""
    Estimado equipo de {institucion.nombre},

    Se ha registrado una nueva valoración terapéutica asociada a su institución.

    🧑 Paciente:
    - Nombre: {instance.nombre}
    - Fecha de Nacimiento: {instance.fecha_nacimiento}
    - Edad: {instance.edad}
    - Servicio: {instance.servicio}
    - Fecha de Valoración: {instance.fecha_valoracion}
    - Diagnóstico: {instance.diagnostico or 'No ingresado'}
    - Recibe Asesoría: {'Sí' if instance.recibe_asesoria else 'No'}

    📎 Observaciones:
    {instance.observaciones or 'Sin observaciones'}

    {"📥 Archivo Adjunto: " + archivo_link if archivo_link else "No se adjuntó archivo."}

    Este es un mensaje automático generado por el sistema Meddes.

    Atentamente,
    Equipo Meddes@
    """

    enviar_correo_valoracion_async.delay(asunto, cuerpo, correo_destino)

