from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm,MensajeForm,CitaForm                   
from .models import Profile, Cita
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from django.conf import settings
from pathlib import Path
from django.core.cache import cache
from .models import Dashboard, Mensaje
from django.shortcuts import render
from .models import Cita,tareas, pagos  # Asegúrate de usar la ruta correcta



@staff_member_required
def dashboard_view(request):
    return render(request, "admin/custom_dashboard.html")

def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user_profile = Profile.objects.get(user=user)
                    return redirect('usuarios:perfil')
                else:
                    return HttpResponse('Disabled account')
            else:
                form = LoginForm()
                return render(request, 'registration/editorial_literario/login_fail.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'registration/editorial_literario/login.html', {'form': form})

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)    
    return render(request, 'usuarios/dashboard.html', {
        'section': 'dashboard',
    })


@login_required
@staff_member_required
def admin_cita_detail(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    context = {
        "title": f"Cita #{cita.id}",
        "breadcrumbs": [
            {"url": "/admin/", "label": "Admin"},
            {"url": "", "label": f"Cita #{cita.id}"},
        ],
        "cards": [
            {
                "title": "Detalle de la cita",
                "icon": "event",
                "items": [
                    {"title": "destinatario", "description": str(cita.destinatario)},
                    {"title": "Fecha", "description": str(cita.fecha)},
                    {"title": "Estado", "description": str(cita.estado or "No definido")}
                ],
            }
        ],
        "cita": cita,
    }
    return render(request, "admin/cita_detail_unfold.html", context)

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    cantidad_mensajes_recibidos = Mensaje.objects.filter(receptor=request.user).count()
    cantidad_mensajes_enviados = Mensaje.objects.filter(emisor=request.user).count()
    cantidad_terapias_realizadas = tareas.objects.filter(user=request.user).count()
    citas_realizadas = Cita.objects.filter(destinatario=request.user).count()

    # Obtener estado de pago desde el modelo `pagos`
    estado_de_pago = None
    try:
        pago = pagos.objects.get(user=request.user)
        estado_de_pago = pago.estado_de_pago
    except pagos.DoesNotExist:
        estado_de_pago = "No registrado"

    return render(request, 'usuarios/profile.html', {
        'profile': profile,
        'cantidad_mensajes_recibidos': cantidad_mensajes_recibidos,
        'cantidad_mensajes_enviados': cantidad_mensajes_enviados,
        'cantidad_terapias_realizadas': cantidad_terapias_realizadas,
        'citas_realizadas': citas_realizadas,
        'estado_de_pago': estado_de_pago,
    })

    
def ver_mensaje(request, pk):
    mensaje = get_object_or_404(Mensaje, pk=pk)

    # Si el mensaje no ha sido leído, lo marcamos como leído
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save()

    return render(request, 'usuarios/mensaje.html', {'mensaje': mensaje})

@login_required
def enviar_mensaje(request):
    destinatario = User.objects.get(id=1)  # <--- usuario fijo al que se envían los mensajes

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = request.user
            mensaje.receptor = User.objects.get(id=1)  # <-- se asigna automáticamente
            mensaje.save()
            return redirect('usuarios:inbox')  # o donde prefieras
    else:
        form = MensajeForm()
    
    return render(request, 'usuarios/enviar_mensaje.html', {'form': form})

@login_required
def inbox_view(request):
    profile = Profile.objects.get(user=request.user)
    mensajes = request.user.mensajes_recibidos.all()

    leidos = mensajes.filter(leido=True).count()
    no_leidos = mensajes.filter(leido=False).count()
    total = mensajes.count()

    return render(request, 'usuarios/inbox.html', {
        'mensajes': mensajes,
        'profile': profile,
        'leidos': leidos,
        'no_leidos': no_leidos,
        'total': total,
    })

@login_required
def config_view(request):
    # Obtener el perfil del usuario actualmente autenticado
    profile = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/config.html', {'profile': profile})




@login_required
def gestionar_citas_view(request):
    citas = Cita.objects.filter(destinatario=request.user).order_by('-fecha')

    citas_confirmadas = citas.filter(estado='confirmada').count()
    citas_pendientes = citas.filter(estado='pendiente').count()
    citas_canceladas = citas.filter(estado='cancelada').count()

    return render(request, 'usuarios/calendar.html', {
        'citas': citas,
        'citas_confirmadas': citas_confirmadas,
        'citas_pendientes': citas_pendientes,
        'citas_canceladas': citas_canceladas,
    })


@login_required
def cancelar_cita_view(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, destinatario=request.user)
    
    if cita.estado == 'cancelada':
        messages.info(request, 'La cita ya está cancelada.')
    else:
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'La cita ha sido cancelada correctamente.')

    return redirect('gestionar_citas')

@login_required
def editar_cita_view(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, destinatario=request.user)

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'La cita ha sido actualizada correctamente.')
            return redirect('gestionar_citas')
    else:
        form = CitaForm(instance=cita)

    return render(request, 'usuarios/editar_cita.html', {'form': form, 'cita': cita})