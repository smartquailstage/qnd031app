

import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.urls import reverse_lazy
import json
import logging
from datetime import datetime

#prueba
BASE_DIR = Path(__file__).resolve().parent.parent


# Load environment variables from the .env_local file.
ENV_FILE_PATH = BASE_DIR / ".env_prod"
load_dotenv(dotenv_path=ENV_FILE_PATH)

# Retrieve the Django secret key from environment variables.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Optionally, you can add a default value or raise an exception if SECRET_KEY is not set
if SECRET_KEY is None:
    raise ValueError("DJANGO_SECRET_KEY is not set in the environment variables.")


class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%dT%H:%M:%S.%f')
        log_record = {
            "time": timestamp,
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)

SITE_DOMAIN = os.environ.get('SITE_DOMAIN', 'http://localhost:8000') 

from usuarios.utils import permission_callback 




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

    
    'citas_regulares',


   # 'appointment',
    'django_extensions',
    #'shop',
    #'orders',
    #'payment',
    #'coupons',
    'django_celery_results',
    'django_celery_beat',



    
    


    

   
    

    'agenda',
    'schedule',
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



from usuarios.utils import permission_callback 

def badge_color_callback(request):
    count = 1  # Cambia este valor para probar diferentes colores

    if count == 0:
        return "info"
    elif count < 2:
        return "info"  # si tienes una clase para warning
    else:
        return "info"

UNFOLD = {
    "SITE_TITLE": "Sistema de Administración Terapéutica MEDDES® (I+D)+A",
    "SITE_HEADER": "MEDDES",
    "SHOW_LANGUAGES": True,
    "SITE_SUBHEADER": "Eterprises Research & Development",
    "SITE_DESCRIPTION": "Sistema de Administración Terapéutica MEDDES® (I+D)+A",
    "SITE_COPYRIGHT": "Copyright © 2025 SmartQuail S.A.S Todos los derechos reservados.",
    "SITE_DROPDOWN": [
        {"icon": "person", "title": _("Usuario del sistema"), "link": reverse_lazy("admin:auth_user_changelist")},
        {"icon": "work", "title": _("Departamentos"), "link": reverse_lazy("admin:auth_group_changelist")},
        {"icon": "people", "title": _("Perfil Administrativos"), "link": reverse_lazy("admin:usuarios_administrativeprofile_changelist")},
        {"icon": "medical_services", "title": _("Servicios Terapeuticos"), "link": reverse_lazy("admin:serviceapp_servicioterapeutico_changelist")},
        {"icon": "map", "title": _("Sucursales- MEDDES®"), "link": reverse_lazy("admin:usuarios_sucursal_changelist")},
        {"icon": "edit", "title": _("Bitacora DEV-V.QND.0.3.1.0.1"), "link": reverse_lazy("admin:usuarios_bitacoradesarrollo_changelist")},
        {"icon": "circle", "title": _("+ A (Automatización)"), "link": reverse_lazy("admin:django_celery_results_taskresult_changelist")},
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
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Registros Administrativos"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Prospecciones"),
                        "icon": "edit",
                        "link": reverse_lazy("admin:usuarios_prospeccion_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_meddes",  # ✅ función real
                        "badge_color": "colors-primary-500",
                        #"permission": "usuarios.unfold_config.permission_callback_pacientes",
                        
                    },
                    {
                        "title": _("Instituciones"),
                        "icon": "school",
                        "link": reverse_lazy("admin:usuarios_prospecion_administrativa_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_prospeccion",
                        "badge_color": "custom-green-success",
                    },
                    {
                        "title": _("Terapéutas"),
                        "icon": "medical_services",
                        "link": reverse_lazy("admin:usuarios_perfil_terapeuta_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback",
                        "badge_color": badge_color_callback,
                      #  "permission": "usuarios.unfold_config.permission_callback",
                    },
                    {
                        "title": _("Pacientes"),
                        "icon": "person",
                        "link": reverse_lazy("admin:usuarios_profile_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_terapeutico",
                        "badge_color": "success",
                    },
                    {
                        "title": _("Agenda"),
                        "icon": "calendar_today",
                        "link": reverse_lazy("admin:usuarios_cita_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_citas",
                        "badge_color": "font-subtle-light",
                       # "permission": "usuarios.unfold_config.permission_callback",
                    },
                    {
                        "title": _("Pagos"), 
                        "icon": "payment", 
                        "link": reverse_lazy("admin:usuarios_pagos_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_pagos",
                        "badge_color": "custom-red-alert",
                        #"permission": "usuarios.unfold_config.permission_callback",
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
                       # "permission": "usuarios.unfold_config.permission_callback",
                    },

                    {
                        "title": _("Actividades"), 
                        "icon": "task", 
                        "link": reverse_lazy("admin:usuarios_tareas_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_tareas",
                        "badge_color": "custom-red-alert",
                      #  "permission": "usuarios.unfold_config.permission_callback",
                        
                    },
                    {
                        "title": _("Asistencias"), 
                        "icon": "calendar_today", 
                        "link": reverse_lazy("admin:usuarios_asistenciaterapeuta_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_asistencias",
                        "badge_color": "custom-red-alert",
                       # "permission": "usuarios.unfold_config.permission_callback",
                    },
                ],
            },
            {
                "title": _("Comunicaciones"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Notificaciones"), 
                        "icon": "notifications", "link": reverse_lazy("admin:usuarios_mensaje_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        #"permission": "usuarios.unfold_config.permission_callback",
                    },
                ],
            },
        ],
    },
    "MENU": [
        {"title": _("Dashboard"), "icon": "dashboard", "link": reverse_lazy("admin:index"), "permission": lambda request: request.user.is_superuser},
        {"title": _("Users"), "icon": "people", "link": reverse_lazy("admin:auth_user_changelist")},
    ],
}






MIDDLEWARE = [
    #'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    #'elasticapm.contrib.django.middleware.TracingMiddleware'
    #'wagtail.core.middleware.site.SiteMiddleware',
    #'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ELASTIC_APM = {
    'SERVICE_NAME': 'qnd031app',
    'SECRET_TOKEN': '',  # déjalo vacío si no usas auth
    'SERVER_URL': 'http://apm-server:8200',
    'ENVIRONMENT': 'production',
    'DEBUG': True,
}




ROOT_URLCONF = os.environ.get('ROOT_URLCONF')


#RESTFRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

#Redis Setup




#DJANGO ADMIN SETUPS

#LOGINGS REDIRECT

LOGIN_REDIRECT_URL = 'usuarios:perfil'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

#from django.urls import reverse_lazy
#LOGIN_REDIRECT_URL = reverse_lazy('course_list')

# Configuración de sesiones usando Redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
REDIS_HOST = os.environ.get('REDIS_HOST')  # Cambia esto según tu configuración
REDIS_PORT  = os.environ.get('REDIS_PORT')        # Puerto por defecto de Redis
REDIS_DB  = os.environ.get('REDIS_DB')

#WEBAPP SETTINGS

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CART_SESSION_ID = 'cart'
SBLCART_SESSION_ID = 'cart'
SBACART_SESSION_ID = 'cart'
SBTCART_SESSION_ID = 'cart'
SBMCART_SESSION_ID = 'cart'

BRAINTREE_MERCHANT_ID = os.environ.get('BRAINTREE_M_ID')
BRAINTREE_PUBLIC_KEY = os.environ.get('BRAINTREE_KEY')
BRAINTREE_PRIVATE_KEY = os.environ.get('BRAINTREE_PRIVATE_KEY')

from braintree import Configuration, Environment
# para desplegar cambiar sandbox con Production
Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)



AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    #'account.authentication.EmailAuthBackend',
    #'social_core.backends.facebook.FacebookOAuth2',
    #'social_core.backends.twitter.TwitterOAuth',
    #'social_core.backends.google.GoogleOAuth2',
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
                
            ],
        },
    },
]


WSGI_APPLICATION = os.environ.get('WSGI_APPLICATION')

#WAGTAIL_ADMIN_BASE_URL =  os.environ.get('DOMAINS')
#WAGTAILIMAGES_MAX_UPLOAD_SIZE = 5 * 1024 * 1024 * 1024  # 5 GB en bytes
#WAGTAILIMAGES_MAX_IMAGE_PIXELS = 1000000000  # 1 millardo de píxeles (1 Gb)





# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


#POSTGRES_READY=str(os.environ.get('POSTGRES_READY_ENV'))





# Configuración de sesiones usando Redis
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
#SESSION_CACHE_ALIAS = "default"




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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-Ec'
TIME_ZONE = 'America/Guayaquil'



USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


DEFAULT_FILE_STORAGE = os.environ.get("MEDIA_STORAGE")
STATICFILES_STORAGE =  os.environ.get("STATICFILES_STORAGE")

# Rutas públicas a los archivos
MEDIA_URL = "https://www-static.sfo3.digitaloceanspaces.com/media/"
STATIC_URL = "https://www-static.sfo3.digitaloceanspaces.com/static/"
