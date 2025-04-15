import csv
import xlsxwriter
import datetime
import datetime
from django.contrib import admin
from django.http import HttpResponse
from .models import Profile, Perfil_Terapeuta, Mensaje, Cita ,prospecion_administrativa, tareas, pagos
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from django.db import models
#from tabbed_admin import TabbedModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import path
from django.template.response import TemplateResponse
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter


#def profile_pdf(obj):
#    return mark_safe('<a href="{}">ver perfil</a>'.format(
#        reverse('usuarios:admin_profile_pdf', args=[obj.id])))
#profile_pdf.short_description = 'Perfil de usuario'

 
def export_to_csv(modeladmin, request, queryset): 
    opts = modeladmin.model._meta 
    response = HttpResponse(content_type='text/csv') 
    response['Content-Disposition'] = 'attachment;' \
        'filename={}.csv'.format(opts.verbose_name) 
    writer = csv.writer(response) 
     
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many] 
    # Write a first row with header information 
    writer.writerow([field.verbose_name for field in fields]) 
    # Write data rows 
    for obj in queryset: 
        data_row = [] 
        for field in fields: 
            value = getattr(obj, field.name) 
            if isinstance(value, datetime.datetime): 
                value = value.strftime('%d/%m/%Y') 
            data_row.append(value) 
        writer.writerow(data_row) 
    return response 
export_to_csv.short_description = 'Export to CSV' 


def export_to_excel(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="{}.xlsx"'.format(opts.verbose_name_plural)

    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    # Obtener los campos del modelo
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # Escribir encabezados
    for i, field in enumerate(fields):
        worksheet.write(0, i, field.verbose_name)

    # Escribir datos
    for row_num, obj in enumerate(queryset, start=1):
        for col_num, field in enumerate(fields):
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            worksheet.write(row_num, col_num, str(value))  # Convertir a cadena de texto

    workbook.close()
    return response

export_to_excel.short_description = 'Exportar a Excel'


# Inline de mensajes enviados
# Inlines de mensajes
class MensajesEnviadosInline(admin.TabularInline):
    model = Mensaje
    fk_name = 'emisor'
    extra = 0

class MensajesRecibidosInline(admin.TabularInline):
    model = Mensaje
    fk_name = 'receptor'
    extra = 0

class CitasCreadasInline(admin.TabularInline):
    model = Cita
    fk_name = 'creador'
    extra = 0
    verbose_name = "Cita creada"
    verbose_name_plural = "Citas creadas"

class CitasRecibidasInline(admin.TabularInline):
    model = Cita
    fk_name = 'destinatario'
    extra = 0
    verbose_name = "Cita recibida"
    verbose_name_plural = "Citas recibidas"

class CustomUserAdmin(BaseUserAdmin):
    inlines = [MensajesEnviadosInline, 
               MensajesRecibidosInline,
               CitasCreadasInline,
               CitasRecibidasInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Perfil_Terapeuta)
class Perfil_TerapeutaAdmin(ModelAdmin):
        # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Warn before leaving unsaved changes in changeform
    warn_unsaved_form = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }

    # Display submit button in filters
    list_filter_submit = False

    # Display changelist in fullwidth
    list_fullwidth = False

    # Set to False, to enable filter as "sidebar"
    list_filter_sheet = True

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail

    # Changeform templates (located inside the form)
  #  change_form_before_template = "some/template.html"
  #  change_form_after_template = "some/template.html"

    # Located outside of the form
  #  change_form_outer_before_template = "some/template.html"
  #  change_form_outer_after_template = "some/template.html"

    # Display cancel button in submit line in changeform
    change_form_show_cancel_button = True # show/hide cancel button in changeform, default: False

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    }

    list_display = ['user', 'especialidad']
    actions = [ export_to_csv, export_to_excel]
    verbose_name = "Registro Administrativo / Ingreso de Terapeuta"
    verbose_name_plural = "Registro Administrativo / Ingreso de Terapeuta"


@admin.register(tareas)
class tareasAdmin(ModelAdmin):
        # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Warn before leaving unsaved changes in changeform
    warn_unsaved_form = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }

    # Display submit button in filters
    list_filter_submit = False

    # Display changelist in fullwidth
    list_fullwidth = False

    # Set to False, to enable filter as "sidebar"
    list_filter_sheet = True

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail

    # Changeform templates (located inside the form)
    #change_form_before_template = "some/template.html"
    #change_form_after_template = "some/template.html"

    # Located outside of the form
    #change_form_outer_before_template = "some/template.html"
    #change_form_outer_after_template = "some/template.html"

    # Display cancel button in submit line in changeform
    change_form_show_cancel_button = True # show/hide cancel button in changeform, default: False

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    }

    list_display = ['profile', 'terapeuta', 'fecha_envio','fecha_entrega','media_terapia']
    actions = [ export_to_csv, export_to_excel]
    verbose_name = "Registro Administrativo / Tarea Terapéutica"
    verbose_name_plural = "Administrativo / Tareas Terapéuticas"


@admin.register(prospecion_administrativa)
class prospecion_administrativaAdmin(ModelAdmin):
        # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False

    # Warn before leaving unsaved changes in changeform
    warn_unsaved_form = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }

    # Display submit button in filters
    list_filter_submit = False

    # Display changelist in fullwidth
    list_fullwidth = False

    # Set to False, to enable filter as "sidebar"
    list_filter_sheet = True

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail

    # Changeform templates (located inside the form)
    change_form_before_template = "some/template.html"
    change_form_after_template = "some/template.html"

    # Located outside of the form
    change_form_outer_before_template = "some/template.html"
    change_form_outer_after_template = "some/template.html"

    # Display cancel button in submit line in changeform
    change_form_show_cancel_button = True # show/hide cancel button in changeform, default: False

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    }

    list_display = ['user', 'especialidad']
    actions = [ export_to_csv, export_to_excel]
    verbose_name = "Prospección Administrativa"
    verbose_name_plural = "Prospecciónes Administrativas"

@admin.register(Mensaje)
class MensajeAdmin(ModelAdmin):
    list_display = ['emisor', 'receptor', 'fecha_envio', 'asunto','leido']
    list_filter_sheet = True
    list_filter_submit = True  # Submit button at the bottom of the filter
    list_filter = (
        ("fecha_envio", RangeDateTimeFilter),
    )


@admin.register(pagos)
class PagosAdmin(ModelAdmin):
    list_display = ['profile', 'cuenta', 'colegio', 'plan','servicio','estado_de_pago','convenio']
    list_filter_sheet = True
    list_filter_submit = True  # Submit button at the bottom of the filter


class CitaAdmin(ModelAdmin):
    change_list_template = "admin/citas_calendar.html"
    list_display = ['creador', 'destinatario', 'fecha', 'estado']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('calendario/', self.admin_site.admin_view(self.calendar_view), name='citas_calendar'),
        ]
        return custom_urls + urls

    def calendar_view(self, request):
        citas = Cita.objects.all()
        eventos = []
        for cita in citas:
            eventos.append({
                "title": f"{cita.creador.username} → {cita.destinatario.username}",
                "start": cita.fecha.isoformat(),
                "url": f"/admin/usuarios/cita/{cita.id}/change/"
            })

        context = dict(
            self.admin_site.each_context(request),
            title='Calendario de Citas',
            eventos=eventos,
        )
        return TemplateResponse(request, "admin/citas_calendar.html", context)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['calendar_link'] = mark_safe(
            '<a class="button" href="calendario/">🗓️ Ver Calendario</a>'
        )
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Cita, CitaAdmin)


class PagosItemInline(admin.TabularInline):
    model = pagos
    raw_id_fields = ['user']
    readonly_fields = ['cuenta', 'sucursal', 'colegio', 'plan', 'convenio', 'servicio', 'estado_de_pago']
    fields = ['cuenta', 'sucursal', 'colegio', 'estado_de_pago']  # Solo mostramos estos 4 campos
    can_delete = False
    extra = 0
    max_num = 0  # Evita que se agreguen nuevos elementos

class TareaItemInline(admin.TabularInline):
    model = tareas
    raw_id_fields = ['user']
    readonly_fields = ['terapeuta', 'titulo', 'fecha_envio', 'descripcion_tarea']
    fields = ['terapeuta', 'titulo', 'fecha_envio', 'descripcion_tarea','media_terapia']  # Mostramos solo estos 4 campos
    can_delete = False
    extra = 0
    max_num = 0

class CitaItemInline(admin.TabularInline):
    model = Cita
    raw_id_fields = ['creador']
    readonly_fields = ['creador', 'destinatario', 'motivo', 'fecha', 'estado']
    fields = ['creador', 'fecha', 'motivo', 'estado']  # Mostramos solo estos 4 campos
    can_delete = False
    extra = 0
    max_num = 0

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
            # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False
    inlines = [TareaItemInline,CitaItemInline,PagosItemInline]

    # Warn before leaving unsaved changes in changeform
    warn_unsaved_form = True  # Default: False

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }

    # Display submit button in filters
    list_filter_submit = False

    # Display changelist in fullwidth
    list_fullwidth = True

    # Set to False, to enable filter as "sidebar"
    list_filter_sheet = True

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Dsable select all action in changelist
    list_disable_select_all = False

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail

    # Changeform templates (located inside the form)
    #change_form_before_template = "some/template.html"
    #change_form_after_template = "some/template.html"

    # Located outside of the form
    #change_form_outer_before_template = "some/template.html"
    #change_form_outer_after_template = "some/template.html"

    # Display cancel button in submit line in changeform
    change_form_show_cancel_button = True # show/hide cancel button in changeform, default: False

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    }

    list_display = ['nombre_paciente', 'apellidos_paciente','edad','unidad_educativa','celular','tipo_servicio','fecha_inicio','fecha_terminacion']
    actions = [ export_to_csv, export_to_excel]
    verbose_name = "Registro Administrativo / Ingreso de Paciente"
    verbose_name_plural = "Registro Administrativo / Ingreso de Paciente"    
   #inlines = [MensajesEnviadosInline, MensajesRecibidosInline]

    fieldsets = (
        ('Ingresar Información Personal del Paciente', {
            'fields': ('user', 'photo', 'ruc','nombre_paciente','apellidos_paciente','nacionalidad','sexo','fecha_nacimiento','edad','unidad_educativa'),
            'classes': ('collapse',), 
        }),
        ('Ingresar Información del Representante Legal', {
            'fields': ('nombres_representante_legal', 'apellidos_representante_legal', 'relacion_del_representante','nacionalidad_representante','ruc_representante', 'actividad_economica','email','telefono','celular','provincia','direccion'),
            'classes': ('collapse',),  # Esto hace que se vea plegable
        }),
        ('Ingresar Información Terapéutica', {
            'fields': ('user_terapeuta', 'valorizacion_terapeutica', 'tipo_servicio', 'fecha_inicio','fecha_terminacion'),
            'classes': ('collapse',),  # Esto hace que se vea plegable
        }),

    )

    


