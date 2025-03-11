

import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

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
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",

    'parler',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    



    'core',
    'wagtail',
    'wagtailmedia',
    "wagtail_modeladmin",
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'django.contrib.humanize',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
   # 'wagtail.locales',
    'wagtail_localize.locales',
    'rosetta',   
    'wagtail.admin',
    'wagtail.contrib.routable_page',
    "wagtail_localize",
    'wagtailgmaps',
    'wagtailmenus',



   
    #'subscription',

    'django_social_share',
    'taggit',
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
    'wagtail.contrib.settings',
    "wagtail_ai",

    'localflavor',
   
    'jquery',
    'phone_field',
    'phonenumber_field',
    'bootstrap5',

    'bootstrap_datepicker_plus',
     "webapp",
      'shop',
    'orders',
    'payment',
    'coupons',
    #WEBAPP
    #'wagtail_modeltranslation',
    #'wagtail_modeltranslation.makemigrations',
    #'wagtail_modeltranslation.migrate',

  
]


PARLER_DEFAULT_LANGUAGE_CODE = 'en'
PARLER_DEFAULT_ACTIVATE = True
PARLER_SHOW_EXCLUDED_LANGUAGE_TABS = False


# Configuración de `parler`
PARLER_LANGUAGES = {
    None: (
        {'code': 'en',},
        {'code': 'es',},
    ),
    'default': {
        'fallbacks': ['en'],  # Los idiomas de reserva
        'hide_untranslated': False,  # Ocultar campos no traducidos
    }
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
    #'wagtail.core.middleware.site.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
   # 'shop.middleware.LocaleRedirectMiddleware', 
]



WAGTAIL_AI = {
    "BACKENDS": {
        "default": {
            "CLASS": "wagtail_ai.ai.llm.LLMBackend",
            "CONFIG": {
                # Model ID recognizable by the "LLM" library.
                "MODEL_ID": os.path.join('WAGTAIL_AI_MODEL_ID'),
                "PROMPT_KWARGS": {"system": "A custom, global system prompt."},
            },
        }
    }
}

ROOT_URLCONF = os.environ.get('ROOT_URLCONF')
LOCALE_PATHS =  (
    os.path.join(BASE_DIR, 'locale/'),
)

#WAGTAIL SETUPS
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}
#SITE_ID = 1
#WagtailAnalitycs
GA_KEY_CONTENT = os.environ.get('GA_KEY_CONTENT_ENV')
GA_VIEW_ID = os.environ.get('GA_VIEW_ID_ENV')


WAGTAIL_SITE_NAME = os.environ.get('WAGTAIL_SITE_NAME ')

#RESTFRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'




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

WAGTAIL_ADMIN_BASE_URL =  os.environ.get('DOMAINS')
WAGTAILIMAGES_MAX_UPLOAD_SIZE = os.environ.get('WAGTAILIMAGES_MAX_UPLOAD_SIZE')
WAGTAILIMAGES_MAX_IMAGE_PIXELS = os.environ.get('WAGTAILIMAGES_MAX_IMAGE_PIXELS')
MODELTRANSLATION_AUTOPOPULATE = False








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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE')
TIME_ZONE = os.environ.get('TIME_ZONE')
USE_I18N = os.environ.get('USE_I18N') 
USE_L10N = os.environ.get('USE_L10N') 
USE_TZ = os.environ.get('USE_TZ') 

WAGTAILLOCALIZE = {
    'ENABLE_TRANSLATION_FIELD': True,  # Activar campos traducibles
    'DEFAULT_LANGUAGE': 'en',  # El idioma predeterminado para la localización
}



WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]


WAGTAIL_I18N_ENABLED = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]






# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


MEDIA_URL = "/media/"
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]  
STATIC_URL = "/static/"
STATIC_ROOT = STATIC_ROOT = BASE_DIR / "static"





