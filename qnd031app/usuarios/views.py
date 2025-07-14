from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import LoginForm,MensajeForm,CitaForm,TareaComentarioForm, AutorizacionForm                 
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
from django.http import HttpResponseForbidden

@login_required
def ultima_cita(request):
    # Obtener la última cita asignada al paciente
    ultima_cita = Cita.objects.filter(destinatario=request.user).order_by('-fecha', '-hora').first()
    
    if not ultima_cita:
        # Redirigir o mostrar un mensaje si no hay citas
        return render(request, 'usuarios/panel_usuario2.html', {'mensaje': 'No tienes citas registradas.'})

    # Renderizar la plantilla con la última cita y el perfil
    return render(request, 'usuarios/panel_usuario2.html', {'ultima_cita': ultima_cita})


def politicas_terminos(request):
    """
    Vista que renderiza la página de Políticas de Seguridad,
    Uso de la Información y Términos y Condiciones.
    """
    return render(request, 'politicas_terminos.html')



@login_required
def ultima_tarea(request):
    try:
        # Obtener el perfil del usuario autenticado
        profile = Profile.objects.get(user=request.user)

        # Buscar la última tarea asignada a este perfil, según fecha de envío o de entrega
        ultima_tarea = tareas.objects.filter(profile=profile).order_by('-fecha_envio', '-fecha_entrega').first()

        if not ultima_tarea:
            return render(request, 'usuarios/panel_usuario2.html', {
                'mensaje': 'No tienes tareas asignadas.'
            })

        return render(request, 'usuarios/panel_usuario2.html', {
            'ultima_tarea': ultima_tarea
        })

    except Profile.DoesNotExist:
        return render(request, 'usuarios/panel_usuario2.html', {
            'mensaje': 'No se encontró el perfil del usuario.'
        })


@staff_member_required
def dashboard_view(request):
    return render(request, "admin/custom_dashboard.html")

def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context

@login_required
def user_logout(request):
    logout(request)
    return redirect('usuarios:login')  

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user_obj = User.objects.get(email=cd['email'])
                user = authenticate(request, username=user_obj.username, password=cd['password'])
            except User.DoesNotExist:
                user = None

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('usuarios:perfil')
                else:
                    return HttpResponse('Cuenta desactivada.')
            else:
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
    return render(request, "admin/test.html", context)

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    cantidad_mensajes_recibidos = Mensaje.objects.filter(receptor=request.user).count()
    cantidad_mensajes_enviados = Mensaje.objects.filter(emisor=request.user).count()
    cantidad_terapias_realizadas = tareas.objects.filter(profile__user=request.user, actividad_realizada=True).count()
    citas_realizadas = Cita.objects.filter(destinatario=request.user).count()

    # Obtener estado de pago desde el modelo `pagos`
    try:
        pago = pagos.objects.filter(profile__user=request.user).latest('created_at')
        if pago.al_dia:
            estado_de_pago = "Al día"
        elif pago.pendiente:
            estado_de_pago = "Pendiente"
        elif pago.vencido:
            estado_de_pago = "Vencido"
        else:
            estado_de_pago = "Sin estado"
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

@login_required
def header(request):
    # Ejemplo: contar pedidos creados en las últimas 24 horas
    last_24_hours = timezone.now() - timedelta(hours=24)
    new_notify_count = Mensaje.objects.filter(receptor=request.user, leido=False).count()

    return render(request, 'usuarios/header.html', {
        'new_notify_count': new_notify_count
    })

@login_required
def msj_success(request):
    return render(request, 'usuarios/success.html')
    
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
            return redirect('usuarios:success')  # o donde prefieras
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
def inbox_record(request):
    profile = Profile.objects.get(user=request.user)

    # Todos los mensajes recibidos (leídos y no leídos)
    mensajes = request.user.mensajes_recibidos.all()
    mensajes_recibidos = Mensaje.objects.filter(receptor=request.user)

    leidos = mensajes_recibidos.filter(leido=True).count()
    no_leidos = mensajes_recibidos.filter(leido=False).count()
    total = mensajes_recibidos.count()

    return render(request, 'usuarios/inbox_total.html', {
        'mensajes': mensajes,
        'profile': profile,
        'leidos': leidos,
        'no_leidos': no_leidos,
        'total': total,
    })



@login_required
def cita_success(request):
    return render(request, 'usuarios/citas/success.html')
    



@login_required
def citas_record(request):
    profile = get_object_or_404(Profile, user=request.user)

    citas = (
        Cita.objects
        .filter(destinatario=request.user)
        .select_related('creador', 'destinatario')
        .order_by('-fecha', '-hora')
    )

    confirmadas = citas.filter(confirmada=True, pendiente=False, cancelada=False)
    pendientes = citas.filter(pendiente=True, confirmada=False, cancelada=False)
    canceladas = citas.filter(cancelada=True, pendiente=False, confirmada=False)

    context = {
        'citas': citas,
        'profile': profile,
        'confirmadas': confirmadas.count(),
        'pendientes': pendientes.count(),
        'canceladas': canceladas.count(),
        'total': citas.count(),
    }

    return render(request, 'usuarios/citas/calendar_total.html', context)


@login_required
def citas_agendadas_total(request):
    profile = get_object_or_404(Profile, user=request.user)

    # 🔸 Filtrar solo las citas pendientes
    citas_pendientes = request.user.citas_creadas.filter(pendiente=True)

    confirmadas = request.user.citas_creadas.filter(confirmada=True).count()
    no_confirmadas = request.user.citas_creadas.filter(confirmada=False).count()
    total = request.user.citas_creadas.count()

    return render(request, 'usuarios/citas/calendar_agendadas.html', {
        'citas': citas_pendientes,  # solo las pendientes
        'profile': profile,
        'confirmadas': confirmadas,
        'no_confirmadas': no_confirmadas,
        'total': total,
    })

@login_required
def agendar_cita(request):
    destinatario = get_object_or_404(User, id=1)  # 👈 Ajusta al destinatario real

    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.creador = request.user
            cita.destinatario = destinatario
            cita.pendiente = True
            cita.confirmada = False
            cita.cancelada = False
            cita.save()
            return redirect('usuarios:cita_success')  # 👈 Asegúrate de tener esta vista definida
    else:
        form = CitaForm()

    return render(request, 'usuarios/citas/agendar_cita.html', {'form': form})


@login_required
def ver_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)

    # Solo el creador o destinatario puede acceder
    if request.user != cita.creador and request.user != cita.destinatario:
        return HttpResponseForbidden("No tienes permiso para ver esta cita.")

    if request.method == "POST":
        accion = request.POST.get("accion")

        if accion == "confirmar":
            cita.confirmada = True
            cita.pendiente = False
            cita.cancelada = False
            messages.success(request, "Cita confirmada correctamente.")
        elif accion == "cancelar":
            cita.cancelada = True
            cita.confirmada = False
            cita.pendiente = False
            messages.warning(request, "Cita cancelada correctamente.")

        cita.save()
        return redirect('usuarios:ver_cita', pk=cita.pk)

    return render(request, 'usuarios/citas/cita.html', {'cita': cita})


@login_required
def confirmar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk, destinatario=request.user)

    if request.method == 'POST':
        # Cambiar el estado a confirmada y actualizar los demás estados
        cita.confirmada = True
        cita.pendiente = False
        cita.cancelada = False
        
        # No tienes is_active en tu modelo, así que elimina o ajusta esta línea si no aplica
        # cita.is_active = True  <-- eliminar o comentar

        cita.save()
        messages.success(request, "Cita confirmada correctamente.")

    return redirect('usuarios:ver_cita', pk=pk)

@login_required
def cancelar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk, destinatario=request.user)
    if request.method == 'POST':
        # Cambiar los campos booleanos para reflejar que la cita está cancelada
        cita.pendiente = False
        cita.confirmada = False
        cita.cancelada = True
        cita.save()
    return redirect('usuarios:ver_cita', pk=pk)


@login_required
def config_view(request):
    # Obtener el perfil del usuario actualmente autenticado
    profile = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/config.html', {'profile': profile})




@login_required
def gestionar_citas_view(request):
    citas = Cita.objects.filter(destinatario=request.user).order_by('-fecha')

    citas_confirmadas = citas.filter(confirmada=True).count()
    citas_pendientes = citas.filter(pendiente=True).count()
    citas_canceladas = citas.filter(cancelada=True).count()

    return render(request, 'usuarios/citas/calendar.html', {
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



@login_required
def tareas_asignadas(request):
    # Filtra todas las tareas asignadas al usuario logueado
    tareas_usuario = tareas.objects.filter(profile__user=request.user)

    # Separar por estado
    tareas_realizadas = tareas_usuario.filter(actividad_realizada=True)
    tareas_pendientes = tareas_usuario.filter(actividad_realizada=False)

    context = {
        'tareas_realizadas': tareas_realizadas,
        'tareas_pendientes': tareas_pendientes,
        'total': tareas_usuario.count(),
        'total_realizadas': tareas_realizadas.count(),
        'total_pendientes': tareas_pendientes.count(),
    }

    return render(request, 'usuarios/tareas/tareas_asignadas.html', context)


@login_required
def tareas_list(request):
    tareas_nuevas = tareas.objects.filter(
        profile__user=request.user,
        actividad_realizada=False
    ).order_by('-fecha_envio')
    tareas_usuario = tareas.objects.filter(profile__user=request.user)
    
    tareas_realizadas = tareas_usuario.filter(actividad_realizada=True)
    tareas_pendientes = tareas_usuario.filter(actividad_realizada=False)

    return render(request, 'usuarios/tareas/tareas_list.html', {
        'tareas_nuevas': tareas_nuevas,
        'total': tareas_usuario.count(),
        'total_realizadas': tareas_realizadas.count(),
        'total_pendientes': tareas_pendientes.count(),

    })


@login_required
def ver_tarea(request, pk):
    # Buscar la tarea asegurando que el usuario autenticado es el dueño (paciente)
    tarea = get_object_or_404(tareas, pk=pk, profile__user=request.user)

    comentarios = tarea.comentarios.all()
    form = TareaComentarioForm()

    if request.method == 'POST':
        form = TareaComentarioForm(request.POST, request.FILES)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.tarea = tarea
            comentario.save()

            # Marcar como realizada si el usuario autenticado es el paciente
            tarea.realizada = True
            tarea.save()

            return redirect('usuarios:ver_tarea', pk=tarea.pk)

    return render(request, 'usuarios/tareas/tarea.html', {
        'tarea': tarea,
        'comentarios': comentarios,
        'form': form,
    })



@login_required
def ver_tarea_interactiva(request, pk):
    tarea = get_object_or_404(tareas, pk=pk)

    comentarios = tarea.comentarios.all()
    form = TareaComentarioForm()

    if request.method == 'POST':
        form = TareaComentarioForm(request.POST, request.FILES)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.tarea = tarea
            comentario.save()

            # Opcional: marcar como realizada si el comentario lo hace el paciente
            if request.user == tarea.paciente:
                tarea.realizada = True
                tarea.save()

            return redirect('usuarios:ver_tarea_interactiva', pk=tarea.pk)

    return render(request, 'usuarios/tareas/tarea_interactiva.html', {
        'tarea': tarea,
        'comentarios': comentarios,
        'form': form,
    })



@login_required
def tareas_realizadas(request):
    # Filtra tareas que fueron realizadas por el usuario autenticado
    tareas_completadas = tareas.objects.filter(profile__user=request.user, actividad_realizada=True)

    return render(request, 'usuarios/tareas/tareas_realizadas.html', {
        'tareas_completadas': tareas_completadas,
    })


@login_required
def marcar_tarea_realizada(request, pk):
    # Verifica que la tarea pertenezca al usuario
    tarea = get_object_or_404(tareas, pk=pk, profile__user=request.user)

    if request.method == 'POST':
        tarea.realizada = True
        tarea.save()
        return redirect('usuarios:tareas_realizadas')  # Redirige a la lista de tareas realizadas

    return redirect('usuarios:ver_tarea', pk=pk)



@login_required
def lista_pagos(request):
    # Filtrar los pagos relacionados al usuario actual (vía profile.user)
    pagos_usuario = pagos.objects.filter(profile__user=request.user).order_by('-created_at')

    # Clasificar según los booleanos
    pagos_pendientes = pagos_usuario.filter(pendiente=True)
    pagos_vencidos = pagos_usuario.filter(vencido=True)
    pagos_realizados = pagos_usuario.filter(al_dia=True)

    return render(request, 'usuarios/pagos/lista_pagos.html', {
        'pagos_usuario': pagos_usuario,
        'pagos_pendientes': pagos_pendientes,
        'pagos_vencidos': pagos_vencidos,
        'pagos_realizados': pagos_realizados,
    })


@login_required
def pagos_pendientes_view(request):
    pagos_pendientes = pagos.objects.filter(profile__user=request.user, pendiente=True).order_by('-fecha_vencimiento')

    return render(request, 'usuarios/pagos/pagos_pendientes.html', {
        'pagos_pendientes': pagos_pendientes,
    })



@login_required
def pagos_vencidos_view(request):
    pagos_vencidos = pagos.objects.filter(profile__user=request.user, vencido=True).order_by('-fecha_vencimiento')

    return render(request, 'usuarios/pagos/pagos_vencidos.html', {
        'pagos_vencidos': pagos_vencidos,
    })




@login_required
def ver_pago(request, pk):
    pago = get_object_or_404(pagos, pk=pk)

    # Verificar que el pago pertenezca al usuario autenticado
    if not pago.profile or pago.profile.user != request.user:
        return render(request, '403.html', status=403)

    # Procesar el formulario de carga de comprobante
    if request.method == 'POST' and not pago.comprobante_pago:
        comprobante = request.FILES.get('comprobante_pago')
        numero = request.POST.get('numero_de_comprobante')

        if comprobante:
            pago.comprobante_pago = comprobante
            pago.numero_de_comprobante = numero
            pago.save()
            messages.success(request, "Comprobante subido correctamente.")
            return redirect('usuarios:ver_pago', pk=pk)
        else:
            messages.error(request, "Por favor sube un archivo válido.")

    return render(request, 'usuarios/pagos/ver_pago.html', {'pago': pago})


@login_required
def subir_comprobante_pago(request, pk):
    pago = get_object_or_404(pagos, pk=pk)

    # Asegurar que el usuario autenticado sea el dueño del pago
    if pago.profile.user != request.user:
        messages.error(request, "No tienes permisos para modificar este pago.")
        return redirect('usuarios:lista_pagos')

    if request.method == 'POST':
        comprobante = request.FILES.get('comprobante_pago')
        numero = request.POST.get('numero_de_comprobante')

        if not comprobante:
            messages.error(request, "Debes adjuntar un comprobante.")
        else:
            if pago.comprobante_pago:
                messages.warning(request, "Ya has subido un comprobante.")
            else:
                pago.comprobante_pago = comprobante
                pago.numero_de_comprobante = numero
                pago.save()
                messages.success(request, "Comprobante subido exitosamente.")
                return redirect('usuarios:ver_pago', pk=pago.pk)

    return render(request, 'usuarios/pagos/subir_comprobante.html', {'pago': pago})




@login_required
def vista_certificados(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = AutorizacionForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('usuarios:vista_certificados')
    else:
        form = AutorizacionForm(instance=profile)

    mensajes = Mensaje.objects.filter(receptor=request.user).order_by('-fecha_envio')  # Para usarlo con tus cards

    return render(request, 'usuarios/certificados/certificados_total.html', {
        'form': form,
        'profile': profile,
        'mensajes': mensajes
    })


@login_required
def certificado_inicial(request):
    perfil = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/documentos/certificado_inicial.html', {'perfil': perfil})

@login_required
def informe_inicial(request):
    perfil = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/documentos/informe_inicial.html', {'perfil': perfil})

@login_required
def informes_seguimiento(request):
    perfil = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/documentos/informes_seguimiento.html', {'perfil': perfil})

@login_required
def certificado_alta(request):
    perfil = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/documentos/certificado_alta.html', {'perfil': perfil})



def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context


from django.views.generic import TemplateView
from unfold.views import UnfoldModelAdminViewMixin

class DashboardPrincipalView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Dashboard Principal"  # Esto aparece como título en la página
    permission_required = ()       # Asegúrate de configurar esto para tu seguridad
    template_name = "usuarios/dashboard_principal.html"