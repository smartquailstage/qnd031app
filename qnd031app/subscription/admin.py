from django.contrib import admin
from .models import subscription_info, Contract
from parler.admin import TranslatableAdmin
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register,ModelAdminGroup
#from wagtail_modeltranslation import TranslationPanel





class SuscriptionsInfoAdmin(ModelAdmin):
    model = subscription_info
    menu_label = 'Billing Info'  # El nombre que aparece en el menú de administración
    menu_icon = 'doc-full'  # El ícono que aparece en el menú
    list_display = ('translations','translations__name', 'slug')  # Qué columnas se muestran en la lista
    search_fields = ('name',)  # Campos por los cuales se puede buscar
    add_to_settings_menu = True 
    menu_item_name = "Mi nombre de menú personalizado" 

class ContractAdmin(ModelAdmin):
    model = Contract
    menu_label = 'Terms & Contracts'  # El nombre que aparece en el menú de administración
    menu_icon = 'clipboard-list'  # El ícono que aparece en el menú
    list_display = ('name', 'slug')  # Qué columnas se muestran en la lista
    search_fields = ('name',)  # Campos por los cuales se puede buscar
    add_to_settings_menu = True 
    menu_item_name = "Mi nombre de menú personalizado"



class LibraryGroup(ModelAdminGroup):
    menu_label = "My Subscription"  # name of the group of ModelAdmins
    menu_icon = "user"  # change as required
    menu_order = 1200 # will put in 3rd place (000 being 1st, 100 2nd)
    items = (SuscriptionsInfoAdmin, ContractAdmin)

modeladmin_register(LibraryGroup)