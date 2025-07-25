

import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.urls import reverse_lazy
from decouple import config, Csv







BASE_DIR = Path(__file__).resolve().parent.parent
# Load environment variables from the .env_local file.
ENV_FILE_PATH = BASE_DIR / ".env_local"
load_dotenv(dotenv_path=ENV_FILE_PATH)


DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='support@smartquail.io')
SERVER_EMAIL = config('SERVER_EMAIL', default='support@smartquail.io')


ADMINS = [
    ("Soporte Meddes", "info@meddes.com.ec"),
    # ("Otro Nombre", "otro@correo.com"),  # Puedes agregar más si deseas
]

# Retrieve the Django secret key from environment variables.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['tusitio.com', '127.0.0.1'] 

# Configura DEBUG usando variable de entorno o por defecto False
DEBUG = config('DEBUG', default=False, cast=bool)

if DEBUG:
    ADMINS = []
else:
    # En producción, define tus administradores correctamente:
    ADMINS = [
        ("Soporte SmartQuail", "support@smartquail.io"),
    ]

    


# Variable que define si estás en entorno local
ENVIRONMENT = config("ENVIRONMENT", default="local")  # local, staging, production

if ENVIRONMENT == "local":
    EMAIL_BACKEND = config("EMAIL_BACKEND")
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT", cast=int)
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
    EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    # Configuración de producción u otros entornos
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = "phys.mauiricio.silva@gmail.com"
    EMAIL_HOST_PASSWORD = "secreto_produccion"
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



# Optionally, you can add a default value or raise an exception if SECRET_KEY is not set
if SECRET_KEY is None:
    raise ValueError("DJANGO_SECRET_KEY is not set in the environment variables.")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.environ.get('DJANGO_LOG_FILE', os.path.join(BASE_DIR, 'logs', 'qnd031.log')),
            'formatter': 'json',
        },
    },
    'formatters': {
        'json': {
            'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}


SITE_DOMAIN = os.environ.get('SITE_DOMAIN', 'http://localhost:8000')  # Cambia esto según tu configuración


# Application definition

INSTALLED_APPS = [


    
    "unfold",  # before django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",

    "unfold.contrib.forms",
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",

    #'webapp',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'serviceapp',
    'rosetta',

    
    #'citas_regulares',


   # 'appointment',
    'django_extensions',
    #'shop',
    #'orders',
    #'payment',
    #'coupons',
    'django_celery_results',
    'django_celery_beat',



    
    


    

   
    

   # 'agenda',
    #'schedule',
    'usuarios',



    #'parler',
    'core',
    'django.contrib.humanize',





   
    #'subscription',

    'django_social_share',
   # 'taggit',
    'widget_tweaks',
    'django_forms_bootstrap',
    'bootstrap4',
    'social_django',
    'sorl.thumbnail',
    'embed_video',
    'qr_code',
    'storages',
    'boto3',
    'rest_framework',
    'ckeditor',
    'localflavor',
   
    'jquery',
    'phone_field',
    'phonenumber_field',
    'bootstrap5',

    'bootstrap_datepicker_plus',
    'djmoney',
    'tinymce',
   

    #WEBAPP
    #'wagtail_modeltranslation',
    #'wagtail_modeltranslation.makemigrations',
    #'wagtail_modeltranslation.migrate',

  
]

#LOGINGS REDIRECT

LOGIN_REDIRECT_URL = 'usuarios:perfil'
LOGIN_URL = 'usuarios:login'
LOGOUT_URL = 'usuarios:logout'





from usuarios.utils import  permission_callback,permission_callback_prospecion



def badge_color_callback(request):
    count = 1  # Cambia este valor para probar diferentes colores

    if count == 0:
        return "info"
    elif count < 2:
        return "info"  # si tienes una clase para warning
    else:
        return "info"



def is_terapeuta(request):
    return request.user.groups.filter(name="terapeutico").exists()

def is_administrativo(request):
    return request.user.groups.filter(name="administrativo").exists()

def is_financiero(request):
    return request.user.groups.filter(name="financiero").exists()

def is_institucional(request):
    return request.user.groups.filter(name="institucional").exists()

def is_superuser(request):
    return request.user.is_superuser

def is_administrativo_o_isuperuser(request):
    return is_administrativo(request) or is_superuser(request)

def is_institucional_o_terapeuta_o_administrativo(request):
    return is_institucional(request) or is_terapeuta(request)  or is_administrativo(request)  or is_superuser(request)

def is_institucional_o_administrativo(request):
    return is_institucional(request)   or is_administrativo(request) or is_superuser(request)

def is_admin_o_terapeuta(request):
    return is_administrativo(request) or is_terapeuta(request) or is_superuser(request)

def is_admin_o_financiero(request):
    return is_administrativo(request) or is_financiero(request) or is_superuser(request)

def is_all(request):
    return is_administrativo(request) or is_financiero(request) or is_superuser(request) or is_terapeuta(request) or is_institucional(request)




UNFOLD = {
    "SITE_TITLE": "Sistema de Administración Terapéutica MEDDES® (I+D)+A",
    "SITE_HEADER": "MEDDES",
    "SHOW_LANGUAGES": True,
    "SITE_SUBHEADER": "Eterprises Research & Development",
    "SITE_DESCRIPTION": "Sistema de Administración Terapéutica MEDDES® (I+D)+A",
    "SITE_COPYRIGHT": "Copyright © 2025 SmartQuail S.A.S Todos los derechos reservados.",
    "DASHBOARD_CALLBACK": "usuarios.views.dashboard_callback",
    "SITE_DROPDOWN": [
        {"icon": "person", "title": _("Usuarios(AUTH)"), "link": reverse_lazy("admin:auth_user_changelist")},
        {"icon": "key", "title": _("Roles(RBAC)"), "link": reverse_lazy("admin:auth_group_changelist")},
        {"icon": "people", "title": _("Administrativos"), "link": reverse_lazy("admin:usuarios_administrativeprofile_changelist")},
        {"icon": "people", "title": _("Institucionales"), "link": reverse_lazy("admin:usuarios_perfilinstitucional_changelist")},
         {"icon": "people", "title": _("Terapeutas"), "link": reverse_lazy("admin:usuarios_perfil_terapeuta_changelist")},
        {"icon": "medical_services", "title": _("Servicios"), "link": reverse_lazy("admin:serviceapp_servicioterapeutico_changelist")},
        
        {"icon": "map", "title": _("Sucursales"), "link": reverse_lazy("admin:usuarios_sucursal_changelist")},
        {"icon": "circle", "title": _("Monitoreo"), "link": reverse_lazy("admin:django_celery_results_taskresult_changelist")},
         {"icon": "support", "title": _("Soporte"), "link": reverse_lazy("admin:usuarios_cliente_changelist")},
    ],
    "SITE_URL": "https://www.meddes.com.ec/",
    "SITE_ICON": {"light": lambda request: static("img/BA-LOGOS/loro.png"), "dark": lambda request: static("img/BA-LOGOS/loro.png")},
    "SITE_LOGO": {"light": lambda request: static("img/BA-LOGOS/logoF.png"), "dark": lambda request: static("img/BA-LOGOS/logo.png")},
    "SITE_SYMBOL": "speed",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x28",
            "type": "image/svg+xml",
            "href": lambda request: static("img/BA-LOGOS/loro.png"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "DASHBOARD_CALLBACK": "usuarios.views.dashboard_callback",
    "ENVIRONMENT": "qnd031app.utils.environment.environment_callback",
    "THEME": "light",
    "LOGIN": {  "image": lambda request: static("img/BA-BG/test.jpg"),
               "password_icon": lambda request: static("icons/eye-solid.svg"),
                "username_icon": lambda request: static("icons/username-icon.svg")
                },
               
    "STYLES": [
        lambda request: static("unfold/css/style.css"),        # archivo original
        lambda request: static("css/unfold_override.css"),     # tu override personalizado
    ],
    "SCRIPTS": [lambda request: static("unfold/js/script.js")],
    "BORDER_RADIUS": "6px",
    "COLORS": {
        "custom": {
            "green-success": "69 162 67",
            "red-alert": "69 162 67",
        },

        "base": {
            "50": "255 255 255",
            "100": "123 204 121",
            "200": "211 213 205",
            "300": "209 213 219",
            "400": "41 168 80",
            "500": "51 55 53",
            "600": "75 85 99",
            "700": "7 121 176",
            "800": "4 168 79",
            "900": "60 59 59",
            "950": "3 7 18",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "229 234 231",
            "600": "61 61 56",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "24 85 2",
            "950": "59 7 100",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "var(--color-base-400)",
            "default-light": "var(--color-base-600)",
            "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)",
            "important-dark": "var(--color-base-100)",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
    "TABS": [
        {
            "models": [{"name": "usuarios.prospecion_administrativa", "detail": True}],
            "items": [
                {
                    "title": _("Perfil Institucional"),
                    "link": reverse_lazy("admin:usuarios_prospecion_administrativa_changelist"),
                   # "permission": permission_callback,
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
"navigation": [

    {
        "title": _("Comunicaciones"),
        "separator": True,
        "collapsible": True,
        "items": [
            {
                "title": _("Bandeja de Entrada"),
                "icon": "inbox",
                "link": reverse_lazy("admin:usuarios_mensaje_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                "badge_color": "custom-red-alert",
                "permission": is_all,
            },
        ],
    },

    {
        "title": _("Registros Administrativos"),
        "separator": True,
        "collapsible": True,
        "items": [
            {
                "title": _("Prospecciones"),
                "icon": "edit",
                "link": reverse_lazy("admin:usuarios_prospeccion_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_meddes",
                "badge_color": "colors-primary-500",
                "permission": is_administrativo_o_isuperuser,
            },
            {
                "title": _("Instituciones"),
                "icon": "school",
                "link": reverse_lazy("admin:usuarios_prospecion_administrativa_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_prospeccion",
                "badge_color": "custom-green-success",
                "permission": is_institucional_o_administrativo,
            },
            {
                "title": _("Historiales"),
                "icon": "book",
                "link": reverse_lazy("admin:usuarios_profile_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_terapeutico",
                "badge_color": "success",
                "permission":  is_institucional_o_terapeuta_o_administrativo,
            },
            {
                "title": _("Agenda"),
                "icon": "calendar_today",
                "link": reverse_lazy("admin:usuarios_cita_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_citas",
                "badge_color": "font-subtle-light",
                "permission": is_administrativo_o_isuperuser,
            },
            {
                "title": _("Pagos"),
                "icon": "payment",
                "link": reverse_lazy("admin:usuarios_pagos_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_pagos",
                "badge_color": "custom-red-alert",
                "permission": is_admin_o_financiero,
            },
        ],
    },
    {
        "title": _("Registros Terapéuticos"),
        "separator": True,
        "collapsible": True,
        "items": [
            {
                "title": _("Valoraciones"),
                "icon": "download",
                "link": reverse_lazy("admin:usuarios_valoracionterapia_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_valoracion",
                "badge_color": "custom-red-alert",
                "permission": is_institucional_o_terapeuta_o_administrativo,
            },
            {
                "title": _("Terapias"),
                "icon": "task",
                "link": reverse_lazy("admin:usuarios_tareas_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_tareas",
                "badge_color": "custom-red-alert",
                "permission": is_institucional_o_terapeuta_o_administrativo,
            },
        ],
    },

],

    },
    "MENU": [
        #{"title": _("Dashboard"), "icon": "dashboard", "link": reverse_lazy("admin:index"), "permission": lambda request: request.user.is_superuser},
        {"title": _("Users"), "icon": "people", "link": reverse_lazy("admin:auth_user_changelist")},
        {
            "label": "Dashboard",
            "url": "/es/inicio/",
            "icon": "home",
        },
    ],
}












PARLER_DEFAULT_LANGUAGE_CODE = 'es'
PARLER_DEFAULT_ACTIVATE = True
PARLER_SHOW_EXCLUDED_LANGUAGE_TABS = False



#AUTH_USER_MODEL = 'usuarios.Cita'


MIDDLEWARE = [
    #'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
   
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    #'wagtail.core.middleware.site.SiteMiddleware',
    #'wagtail.contrib.redirects.middleware.RedirectMiddleware',
   # 'shop.middleware.LocaleRedirectMiddleware', 
]


LANGUAGE_CODE = 'es'

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

TIME_ZONE = 'America/Guayaquil'  # O 'America/Mexico_City', 'America/Argentina/Buenos_Aires', etc.

USE_I18N = True
USE_L10N = True
USE_TZ = True


from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('es', _('Español')),
    ('en', _('Inglés')),
]

ROOT_URLCONF = os.environ.get('ROOT_URLCONF')
#SITE_ID = 1
#WagtailAnalitycs



#WAGTAIL_SITE_NAME = os.environ.get('WAGTAIL_SITE_NAME ')

#RESTFRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}






AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]





TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR /  "qnd031app","templates"], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'usuarios.context_processors.mensajes_nuevos_processor',
                'usuarios.context_processors.datos_panel_usuario', 
                'usuarios.context_processors.user_profile_data',
                'usuarios.context_processors.citas_context',
                'usuarios.context_processors.tareas_context',
                'usuarios.context_processors.pagos_context',  
                'usuarios.context_processors.profile_uploads_context',
                'usuarios.context_processors.ultima_cita',
                'usuarios.context_processors.ultima_tarea',
                
            ],
        },
    },
]

WSGI_APPLICATION = os.environ.get('WSGI_APPLICATION')










# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


#POSTGRES_READY=str(os.environ.get('POSTGRES_READY_ENV'))





# Configuración de sesiones usando Redis
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
#SESSION_CACHE_ALIAS = "default"
#REDIS_HOST = os.environ.get('REDIS_HOST')  # Cambia esto según tu configuración
#REDIS_PORT  = os.environ.get('REDIS_PORT')        # Puerto por defecto de Redis
#REDIS_DB  = os.environ.get('REDIS_DB')



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


MEDIA_URL = "/media/"
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]  
STATIC_URL = "/static/"
STATIC_ROOT = STATIC_ROOT = BASE_DIR / "static"





