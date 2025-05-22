def permission_callback(request):
    return request.user.has_perm("usuarios.change_model")