from usuarios.models import Perfil_Terapeuta

def badge_callback(request):
    try:
        return Perfil_Terapeuta.objects.count()
    except:
        return 0

def permission_callback(request):
    return request.user.has_perm("usuarios.change_perfil_terapeuta")

def dashboard_callback(request, context):
    context.update({
        "sample": "example"
    })
    return context

def environment_callback(request):
    return ["Producción", "danger"]