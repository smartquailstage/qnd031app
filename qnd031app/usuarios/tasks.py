# usuarios/tasks.py
from celery import shared_task
from django.core.mail import send_mail
import requests
from django.conf import settings

@shared_task
def enviar_correo_async(emisor, receptor_email, asunto, cuerpo):
    mensaje = f"De: {emisor}\n\n{cuerpo}"
    send_mail(
        subject=asunto,
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[receptor_email]
    )

@shared_task
def enviar_whatsapp_async(telefono, mensaje):
    # Cambia esta URL/token a tu proveedor real
    url = "https://api.example.com/sendMessage"
    token = "YOUR_API_TOKEN"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "phone": telefono,
        "body": mensaje
    }

    try:
        requests.post(url, json=data, headers=headers)
    except requests.RequestException as e:
        print("Error enviando WhatsApp:", e)
