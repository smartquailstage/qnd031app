

import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.urls import reverse_lazy


BASE_DIR = Path(__file__).resolve().parent.parent
# Load environment variables from the .env_local file.
ENV_FILE_PATH = BASE_DIR / ".env_stage"
load_dotenv(dotenv_path=ENV_FILE_PATH)



# Retrieve the Django secret key from environment variables.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Optionally, you can add a default value or raise an exception if SECRET_KEY is not set
if SECRET_KEY is None:
    raise ValueError("DJANGO_SECRET_KEY is not set in the environment variables.")




# Application definition

INSTALLED_APPS = [
   
    "unfold",  # before django.contrib.admin

    #'webapp',



    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",
    'appointment',
    'django_q',
    'django_extensions',
   # 'django_q',  # Optional: for email reminders

    #'shop',
    #'orders',
    #'payment',
    #'coupons',
    'django_celery_results',
    'django_celery_beat',
    'usuarios',

    

   
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',



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
   

    #WEBAPP
    #'wagtail_modeltranslation',
    #'wagtail_modeltranslation.makemigrations',
    #'wagtail_modeltranslation.migrate',

  
]


#LOGINGS REDIRECT

LOGIN_REDIRECT_URL = 'usuarios:perfil'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

UNFOLD = {
    "SITE_TITLE": "MEDDES-ERP",
    "SITE_HEADER": "MEDDES",
    "SITE_SUBHEADER": "ERP Center Data",
    "SITE_DROPDOWN": [
        {
            "icon": "diamond",
            "title": _("My site"),
            "link": "admin:shop_category_changelist",
        },
        # ...
    ],
    "SITE_URL": "/",
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    "SITE_ICON": {
        "light": lambda request: static("img/BA-LOGOS/loro.png"),
        "dark": lambda request: static("img/BA-LOGOS/loro.png"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("img/BA-LOGOS/logo.png"),
        "dark": lambda request: static("img/BA-LOGOS/logo.png"),
    },
    "SITE_SYMBOL": "speed",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("img/BA-LOGOS/loro.png"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": False,
    "DASHBOARD_CALLBACK": "usuarios.views.dashboard_callback",
    
    "ENVIRONMENT": "qnd031app.utils.environment.environment_callback",

    "THEME": "light",
    "LOGIN": {
        "image": lambda request: static("img/BA-BG/test.png"),
       # "redirect_after": lambda request: reverse_lazy("admin:usuarios_changelist"),
    },
    "STYLES": [
        lambda request: static("css/style.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/script.js"),
    ],
    "BORDER_RADIUS": "6px",
    "COLORS": {
        "base": {
            "50": "240 240 240",
            "100": "236 236 236",
            "200": "211 213 205",
            "300": "209 213 219",
            "400": "41 168 80",
            "500": "0, 180, 81",
            "600": "75 85 99",
            "700": "7 121 176",
            "800": "4 168 79",
            "900": "38 134 4",
            "950": "3 7 18",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "229 234 231",
            "600": "48 169 81",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "24 85 2",
            "950": "59 7 100",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
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
                        "title": _("Ingreso de Usuarios"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Ingreso de Departamentos"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Ingreso de Pacientes"),
                        "icon": "list",
                        "link": reverse_lazy("admin:usuarios_profile_changelist"),
                    },
                    {
                        "title": _("Ingreso de Terapistas"),
                        "icon": "list",
                        "link": reverse_lazy("admin:usuarios_perfil_terapeuta_changelist"),
                    },


                    {
                        "title": _("Ingreso de Prospecto de Paciente"),
                        "icon": "edit",    
                        "link": reverse_lazy("admin:usuarios_prospecion_administrativa_changelist"),
                    },
                    {
                        "title": _("Ingreso de Pagos por servicios Terapéuticos"),
                        "icon": "payment",
                        "link": reverse_lazy("admin:usuarios_pagos_changelist"),
                    },
                ],
            },
            {
                "title": _("Registros Terapéuticos"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Ingreso de Tareas Terapéuticas "),
                        "icon": "task",
                        "link": reverse_lazy("admin:usuarios_tareas_changelist"),
                    },
                ],
            },
            {
                "title": _("Comunicaciones"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Bandeja de Mensajes"),
                        "icon": "inbox",
                        "link": reverse_lazy("admin:usuarios_mensaje_changelist"),
                    },
                ],
            },
        ],
    },

 
    "MENU": [
        {
            "title": _("Dashboard"),
            "icon": "dashboard",
            "link": reverse_lazy("admin:index"),
            "permission": lambda request: request.user.is_superuser,
        },
        {
            "title": _("Users"),
            "icon": "people",
            "link": reverse_lazy("admin:auth_user_changelist"),
        },
    ],


}







def badge_callback(request):
    return 3





PARLER_DEFAULT_LANGUAGE_CODE = 'en'
PARLER_DEFAULT_ACTIVATE = True
PARLER_SHOW_EXCLUDED_LANGUAGE_TABS = False



#AUTH_USER_MODEL = 'usuarios.Cita'


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
    #'wagtail.core.middleware.site.SiteMiddleware',
    #'wagtail.contrib.redirects.middleware.RedirectMiddleware',
   # 'shop.middleware.LocaleRedirectMiddleware', 
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = os.environ.get('WSGI_APPLICATION')










# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


#POSTGRES_READY=str(os.environ.get('POSTGRES_READY_ENV'))





# Configuración de sesiones usando Redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
REDIS_HOST = os.environ.get('REDIS_HOST')  # Cambia esto según tu configuración
REDIS_PORT  = os.environ.get('REDIS_PORT')        # Puerto por defecto de Redis
REDIS_DB  = os.environ.get('REDIS_DB')



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





