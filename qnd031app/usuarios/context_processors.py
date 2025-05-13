from .models import Mensaje

def mensajes_nuevos_processor(request):
    if request.user.is_authenticated:
        count = Mensaje.objects.filter(receptor=request.user, leido=False).count()
    else:
        count = 0
    return {'mensajes_nuevos': count}