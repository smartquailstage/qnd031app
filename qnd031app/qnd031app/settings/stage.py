from .base_stage import *




ENV_FILE_PATH = BASE_DIR / ".env_stage"
load_dotenv(str(ENV_FILE_PATH))

DEBUG=os.environ.get("DEBUG")

ALLOWED_HOSTS = os.environ.get("ENV_ALLOWED_HOSTS", "").split(",") if os.environ.get("ENV_ALLOWED_HOSTS") else []


from django.urls import reverse_lazy
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "SmartBusinessAnalytics",
    "SITE_HEADER": "SmartBusinessAnalytics",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("img/logo.png"),
        "dark": lambda request: static("img/logo.png"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("img/m2.png"),
        "dark": lambda request: static("img/m2.png"),
    },
    "SITE_SYMBOL": "speed",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("img/logo.png"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "ENVIRONMENT": "danger.environment_callback",
    "THEME": "light",
    "LOGIN": {
        "image": lambda request: static("img/logo_splash.png"),
    },
    "STYLES": [
        lambda request: static("css/style.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/script.js"),
    ],
    "BORDER_RADIUS": "3px",
    "COLORS": {
        "base": {
            "50": "#F9FAFB",
            "100": "#F3F4F6",
            "200": "#E5E7EB",
            "300": "#D1D5DB",
            "400": "#9CA3AF",
            "500": "#6B7280",
            "600": "#4B5563",
            "700": "#374151",
            "800": "#1F2937",
            "900": "#111827",
            "950": "#030718",
        },
        "primary": {
            "50": "#FAF5FF",
            "100": "#F3E8FF",
            "200": "#E9D5FF",
            "300": "#D8B4FE",
            "400": "#C084FC",
            "500": "#C20002",
            "600": "#D10505",
            "700": "#7E22CE",
            "800": "#6B21A8",
            "900": "#581C87",
            "950": "#3B0764",
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
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("E-Commerce Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Product Categories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:shop_category_changelist"),
                    },
                    {
                        "title": _("Products Details"),
                        "icon": "check",
                        "link": reverse_lazy("admin:shop_product_changelist"),
                    },
                    {
                        "title": _("Orders Purchases"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:orders_order_changelist"),
                    },
                    {
                        "title": _("Coupons"),
                        "icon": "tag",
                        "link": reverse_lazy("admin:coupons_coupon_changelist"),
                    },
                ],
            },
            {
                "title": _("E-commerce Analytics"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Products vs Sales"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Total product Sales"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Total Sales"),
                        "icon": "analytics",
                        "link": reverse_lazy("admin:shop_category_changelist"),
                    },
                ],
            },
            {
                "title": _("E-commerce Statistics"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Products vs Sales"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Total product Sales"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Total Sales"),
                        "icon": "analytics",
                        "link": reverse_lazy("admin:shop_category_changelist"),
                    },
                ],
            },
            {
                "title": _("Users and Groups Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("SmartBusinessMedia"),
                        "icon": "analytics",
                        "link": reverse_lazy("admin:shop_category_changelist"),
                    },
                ],
            },
        ],
    },

}



def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """
    context.update(
        {
            "sample": "example",  # this will be injected into templates/admin/index.html
        }
    )
    return context


def environment_callback(request):
    """
    Callback has to return a list of two values represeting text value and the color
    type of the label displayed in top right corner.
    """
    return ["Production", "danger"] # info, danger, warning, success


def badge_callback(request):
    return 3

def permission_callback(request):
    return request.user.has_perm("shop.change_model")




#import wagtail_ai

#WAGTAIL_AI_PROMPTS = wagtail_ai.DEFAULT_PROMPTS + [
#    {
#        "label": "Simplify",
#        "description": "Rewrite your text in a simpler form",
#        "prompt": "Rewrite the following text to make it simper and more succinct",
#        "method": "replace",
#    }
#]


#CSRF_COOKIE_DOMAIN=".www.smartquail.io"
#CSRF_COOKIE_SECURE = True
#CSRF_TRUSTED_ORIGINS = ['https://www.smartquail.io','https://146.190.164.22']
#CORS_ALLOWED_ORIGINS = [
#    'https://www.smartquail.io','https://146.190.164.22'
    # Otros orígenes permitidos si los hay
#]


WAGTAILEMBEDS_RESPONSIVE_HTML = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Obtención de variables de entorno para la configuración de PostgreSQL
DB_USERNAME = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_DATABASE = os.environ.get("POSTGRES_DB")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_ENGINE = os.environ.get("POSTGRES_ENGINE")

# Verificación de disponibilidad de las variables necesarias para PostgreSQL
DB_IS_AVAILABLE = all([
    DB_USERNAME,
    DB_PASSWORD,
    DB_DATABASE,
    DB_HOST,
    DB_PORT
])

# Configuración condicional para PostgreSQL
if DB_IS_AVAILABLE:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': DB_DATABASE,
            'USER': DB_USERNAME,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }

#Static files DevMod


# settings.py

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# celery setup


