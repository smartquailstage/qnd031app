# project/utils/environment.py

def environment_callback(request):
    import os
    env = os.getenv('DJANGO_ENV', 'QND031MD(Desarollo)')

    if env == 'production':
        return ["MEDDES® (I+D)+A ", "success"]
    elif env == 'staging':
        return ["Vesion.QND.0.3.1.0.3(Pruebas)", "warning"]
    elif env == 'demo':
        return ["Vesion.QND.0.3.1.0.3(Demostración)", "info"]
    elif env == 'suspention':
        return ["Vesion.QND.0.3.1.0.3(Inhabilitado por falta de pago) ", "danger"]
    
    else:
        return ["Vesion.QND.0.3.1.0(Desarollo)", "info"]



