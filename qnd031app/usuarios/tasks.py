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




from .models import tareas
from django.core.files import File
from celery import shared_task
import subprocess
from tempfile import NamedTemporaryFile
import os
import requests

@shared_task
def generar_thumbnail_video(tarea_id):
    try:
        tarea = tareas.objects.get(pk=tarea_id)

        if not tarea.media_terapia:
            print(f"[INFO] Tarea {tarea_id} no tiene video.")
            return

        video_url = tarea.media_terapia.url
        print(f"[INFO] Descargando video desde {video_url}")

        # Descargar el video desde Spaces
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
                for chunk in r.iter_content(chunk_size=8192):
                    temp_video.write(chunk)
                temp_video_path = temp_video.name

        # Crear archivo temporal para el thumbnail
        temp_thumb = NamedTemporaryFile(suffix=".jpg", delete=False)

        cmd = [
            'ffmpeg',
            '-i', temp_video_path,
            '-ss', '00:00:01.000',
            '-vframes', '1',
            '-q:v', '2',
            temp_thumb.name
        ]

        subprocess.run(cmd, check=True)

        if not os.path.exists(temp_thumb.name):
            print("[ERROR] ffmpeg no generó el archivo thumbnail.")
            return

        with open(temp_thumb.name, 'rb') as f:
            file_name = f"thumb_{tarea_id}.jpg"
            tarea.thumbnail_media.save(file_name, File(f), save=True)

        print(f"[SUCCESS] Thumbnail generado para tarea {tarea_id}")

    except Exception as e:
        print(f"[ERROR] Generando thumbnail para tarea {tarea_id}: {e}")

    finally:
        # Limpieza de archivos temporales
        try:
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
            if os.path.exists(temp_thumb.name):
                os.remove(temp_thumb.name)
        except Exception as e:
            print(f"[CLEANUP ERROR] {e}")




@shared_task(bind=True, max_retries=3, default_retry_delay=60)  # 3 intentos, 60s entre cada uno
def enviar_correo_async(self, emisor, receptor_email, asunto, cuerpo_html):
    try:
        cuerpo_texto = "Este es un mensaje alternativo en texto plano."

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
        logger.error("❌ Error al enviar correo a %s: %s", receptor_email, str(e))
        raise self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)  # 3 intentos, 30s entre cada uno
def enviar_whatsapp_async(self, telefono, mensaje):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=mensaje,
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{telefono}",
        )

        logger.info(f"✅ WhatsApp enviado a {telefono}: SID={message.sid}")

    except Exception as e:
        logger.error(f"❌ Error enviando WhatsApp a {telefono}: {e}")
        raise self.retry(exc=e)

@shared_task
def enviar_correo_valoracion_async(asunto, cuerpo, destinatario):
    send_mail(
        subject=asunto,
        message=cuerpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[destinatario],
        fail_silently=False,
    )
