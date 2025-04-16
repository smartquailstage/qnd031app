# -*- coding: utf-8 -*-
# usuarios/tasks.py
from celery import shared_task
from django.core.mail import send_mail,BadHeaderError,EmailMultiAlternatives
import requests
from django.conf import settings
from twilio.rest import Client
from django.core.mail.message import EmailMessage
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from email.header import Header
from email.utils import formataddr


from django.utils.html import strip_tags
#from django.core.mail.backends.smtp import EmailBackend
import logging

logger = logging.getLogger(__name__)


@shared_task
def enviar_correo_async(emisor, receptor_email, asunto, cuerpo_html):
    try:
        cuerpo_texto = "Este es un mensaje alternativo en texto plano."

        # Garantizamos codificación segura con Header y formataddr
        asunto = Header(asunto, 'utf-8').encode()
        emisor = formataddr((str(Header(emisor, 'utf-8')), settings.DEFAULT_FROM_EMAIL))

        email = EmailMultiAlternatives(
            subject=asunto,
            body=cuerpo_texto,
            from_email=emisor,
            to=[receptor_email]
        )

        email.attach_alternative(cuerpo_html, "text/html")
        email.encoding = 'utf-8'

        email.send()
        logger.info("📧 Correo enviado exitosamente a %s", receptor_email)

    except Exception as e:
        logger.error("❌ Error general al enviar el correo a %s: %s", receptor_email, str(e))


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
