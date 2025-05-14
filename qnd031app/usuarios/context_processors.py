from datetime import timedelta, date
from .models import Mensaje

def mensajes_nuevos_processor(request):
    if request.user.is_authenticated:
        hoy = date.today()
        desde = hoy - timedelta(days=7)

        mensajes_queryset = Mensaje.objects.filter(
            receptor=request.user,
            leido=False,
            fecha_envio__date__gte=desde
        ).order_by('-fecha_envio')

        count = mensajes_queryset.count()
        mensajes = mensajes_queryset[:6]
    else:
        count = 0
        mensajes = []

    return {
        'mensajes_nuevos': count,
        'mensajes_recientes': mensajes
    }
