# usuarios/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mensaje
from .tasks import enviar_correo_async, enviar_whatsapp_async

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

