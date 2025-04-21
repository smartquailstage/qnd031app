from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm,MensajeForm                   
from .models import Profile
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from django.conf import settings
from pathlib import Path
from django.core.cache import cache
from .models import Dashboard, Mensaje



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
def profile_view(request):
    # Obtener el perfil del usuario actualmente autenticado
    profile = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/profile.html', {'profile': profile})

def ver_mensaje(request, pk):
    mensaje = get_object_or_404(Mensaje, pk=pk)
    return render(request, 'admin/ver_mensaje.html', {'mensaje': mensaje})

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
            return redirect('bandeja_entrada')  # o donde prefieras
    else:
        form = MensajeForm()
    
    return render(request, 'usuarios/enviar_mensaje.html', {'form': form})

@login_required
def inbox_view(request):
    profile = Profile.objects.get(user=request.user)
    mensajes = request.user.mensajes_recibidos.all()

    return render(request, 'usuarios/inbox.html', {
        'mensajes': mensajes,
        'profile': profile,
    })

@login_required
def config_view(request):
    # Obtener el perfil del usuario actualmente autenticado
    profile = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/config.html', {'profile': profile})