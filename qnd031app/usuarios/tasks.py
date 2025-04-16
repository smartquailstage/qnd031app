# -*- coding: utf-8 -*-
# usuarios/tasks.py
from celery import shared_task
from django.core.mail import send_mail,BadHeaderError
import requests
from django.conf import settings
from twilio.rest import Client
from django.core.mail.message import EmailMessage
from django.utils.html import format_html
from django.utils.safestring import mark_safe


from django.utils.html import strip_tags
#from django.core.mail.backends.smtp import EmailBackend
import logging

logger = logging.getLogger(__name__)




@shared_task
def enviar_correo_async(emisor, receptor_email, asunto, cuerpo):
    try:
        # Crea el mensaje de correo
        email = EmailMessage(
            subject=asunto,
            body=cuerpo,  # Esto es el texto que se mostrará si no soporta HTML
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[receptor_email]
        )

        # Asegúrate de que el cuerpo sea un HTML
        email.content_subtype = "html"
        email.encoding = 'utf-8'

        # Usamos attach_alternative para enviar el contenido HTML
        #email.attach_alternative(cuerpo, "text/html")

        # Enviar el correo
        email.send()
        logger.info("📧 Correo enviado exitosamente a %s", receptor_email)

    except Exception as e:
        logger.error("❌ Error general al enviar el correo: %s", e)

@shared_task
def enviar_whatsapp_async(telefono, mensaje):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=mensaje,
            from_=settings.TWILIO_WHATSAPP_FROM,  # Ej: 'whatsapp:+14155238886'
            to=f"whatsapp:{telefono}",             # Ej: 'whatsapp:+593991234567'
        )

        logger.info(f"✅ Mensaje WhatsApp enviado a {telefono}: SID={message.sid}")

    except Exception as e:
        logger.error(f"❌ Error enviando WhatsApp a {telefono}: {e}")
