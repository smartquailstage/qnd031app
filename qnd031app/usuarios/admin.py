import csv
import xlsxwriter
import datetime
import datetime
from django.contrib import admin
from django.http import HttpResponse
from .models import Profile, BitacoraDesarrollo, Perfil_Terapeuta, Mensaje,ServicioTerapeutico, Sucursal , ValoracionTerapia ,DocenteCapacitado, Cita,ComentarioCita, TareaComentario ,AsistenciaTerapeuta,prospecion_administrativa,Prospeccion, tareas, pagos
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
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.utils.html import format_html
from unfold.sections import TableSection, TemplateSection
from .sites import custom_admin_site
from django.contrib.auth.admin import UserAdmin
from unfold.sites import UnfoldAdminSite
from schedule.models import Calendar, Event, Rule, Occurrence
from schedule.admin import CalendarAdmin 
from django.utils.timezone import localtime
from django.utils.timezone import make_aware
from django import forms
from django.utils import timezone
from unfold.components import BaseComponent, register_component
from unfold.sections import TableSection, TemplateSection
from django.utils.timezone import now
from .forms import ServicioTerapeuticoForm, ProspecionAdministrativaForm




@admin.register(ServicioTerapeutico)
class ServicioTerapeuticoAdmin(ModelAdmin):
    form = ServicioTerapeuticoForm
    list_display = ['servicio', 'costo_por_sesion', 'activo']
    list_filter = ['activo']
    search_fields = ['servicio']


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aquí puedes agregar lógica según el usuario actual
        user = getattr(self, 'current_user', None)
        if user and not user.is_superuser:
            for field in ['is_active', 'is_staff', 'is_superuser']:
                self.fields[field].disabled = True

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user  # Pasamos el usuario actual al form
        return form

# Re-registramos el modelo User con el nuevo admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



class CustomAdminSite(UnfoldAdminSite):
    site_header = "Panel de Administración"
    site_title = "QNODES"
    index_title = "Dashboard"


    def each_context(self, request):
        context = super().each_context(request)
        # Aquí podés agregar tus citas si querés pasarlas al template
        from usuarios.models import Cita  # ajustá si tu modelo se llama distinto

        context["citas"] = Cita.objects.all()
        return context

custom_admin_site = CustomAdminSite(name="custom_admin_site")

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


@admin.register(ValoracionTerapia)
class ValoracionTerapiaAdmin(ModelAdmin):
    list_display = ['tipo_valoracion','perfil_terapeuta','nombre', 'fecha_valoracion']
    readonly_fields = ['edad']
    actions = [export_to_csv, export_to_excel]

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    }

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
    search_fields = ('paciente__nombre','sucursal', 'terapeuta__nombres_completos')  # Ajusta a tus campos
    list_display = ['get_full_name', 'especialidad','sucursal', 'especialidad']
    
    actions = [ export_to_csv, export_to_excel]
    verbose_name = "Registro Administrativo / Ingreso de Terapeuta"
    verbose_name_plural = "Registro Administrativo / Ingreso de Terapeuta"

    def get_full_name(self, obj):
        return obj.user.get_full_name()  # assumes a related 'user' field with a get_full_name() method
    get_full_name.short_description = 'Terapeuta Registrado' 

@admin.register(AsistenciaTerapeuta)
class AsistenciaTerapeutaAdmin(ModelAdmin):
    # Configuraciones de visualización y comportamiento
    #change_list_template = "admin/dashboard_calendar.html"
    change_form_show_cancel_button = True

    # Configuración de campos
    list_display = ('terapeuta', 'fecha', 'hora_entrada', 'hora_salida')
    list_filter = ('fecha', 'terapeuta')
    search_fields = ('terapeuta__nombres_completos',)
    autocomplete_fields = ['terapeuta']
    actions = [export_to_csv, export_to_excel]

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    }


@admin.register(BitacoraDesarrollo)
class BitacoraDesarrolloAdmin(ModelAdmin):

    def progreso_bar(self, obj):
        color_class = (
           "bg-green-500" if obj.progreso >= 80
           else "bg-yellow-500" if obj.progreso >= 40
           else "bg-red-500"
        )
        progreso = int(obj.progreso or 0)  # aseguramos un entero por si es None

        return format_html(
        '''
        <div class="w-full bg-gray-200 rounded-full h-4 mb-1">
            <div class="{} h-4 rounded-full" style="width: {}%;"></div>
        </div>
        <span class="text-xs text-gray-600">{}%</span>
        ''',
        color_class, progreso, progreso
       )
    progreso_bar.short_description = "Progreso"
    progreso_bar.admin_order_field = 'progreso'

    # Configuración Unfold avanzada
    compressed_fields = True
    warn_unsaved_form = True
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }
    list_filter_submit = False
    list_fullwidth = False
    list_filter_sheet = True
    list_horizontal_scrollbar_top = False
    list_disable_select_all = False

    # List view
    list_display = (
        'autor',
        'titulo',
        'fecha',
        'version_relacionada',
        'tipo_tecnologia',
        'fecha_entrega',
        'progreso_bar',  # Ahora como string, no como método directo
        'estado',
    )

    # Filtros
    list_filter = (
        'fecha',
        'autor',
        'tipo_cambio',
        'version_relacionada',
        'tipo_tecnologia'
    )

    # Acciones personalizadas
    actions = [export_to_csv, export_to_excel]

    # Campos readonly
    readonly_fields = ('fecha', 'fecha_entrega', 'version_relacionada', 'progreso', 'estado')

    # Overrides para campos especiales
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    }


    

class TareasComentariosInline(admin.TabularInline):
    model = TareaComentario
    extra = 1
    fields = ('tarea', 'mensaje', 'archivo', 'fecha')
    readonly_fields = ('fecha',)
    show_change_link = False
    


@admin.register(tareas)
class tareasAdmin(ModelAdmin):
    inlines = [TareasComentariosInline] 
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

    list_display = ['paciente', 'terapeuta', 'fecha_envio','fecha_entrega','media_terapia']
    actions = [ export_to_csv, export_to_excel]
    verbose_name = "Registro Administrativo / Tarea Terapéutica"
    verbose_name_plural = "Administrativo / Tareas Terapéuticas"


@admin.register(Prospeccion)
class ProspeccionAdmin(ModelAdmin):
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
    # change_form_before_template = "some/template.html"
    # change_form_after_template = "some/template.html"

    # Located outside of the form
    # change_form_outer_before_template = "some/template.html"
    # change_form_outer_after_template = "some/template.html"

    # Display cancel button in submit line in changeform
    change_form_show_cancel_button = True  # show/hide cancel button in changeform, default: False

    # Formfield overrides for widgets (e.g. WYSIWYG editor)
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,  # Asegúrate de tener este widget importado si lo usas
        },
        ArrayField: {
            "widget": ArrayWidget,  # Asegúrate de tener este widget importado si lo usas
        }
    }

    # Cambia los campos que se muestran en la lista de objetos
    list_display = [
        'nombre_institucion', 'distrito', 'telefono', 'sector', 'tl_fecha_contacto'
    ]

    # Opcionales: acciones personalizadas para exportar a CSV o Excel
    actions = ['export_to_csv', 'export_to_excel']

    # Personaliza el nombre del modelo en la interfaz de admin
    verbose_name = "Prospección Administrativa"
    verbose_name_plural = "Prospecciones Administrativas"

    # Agregar filtros y búsqueda si lo deseas
    list_filter = ['distrito', 'estado', 'sector']
    search_fields = ['nombre_institucion', 'distrito', 'telefono', 'sector']

    # Opcional: si deseas personalizar el orden en que aparecen los objetos
    ordering = ['nombre_institucion']

class DocenteCapacitadoInline(admin.TabularInline):
    model = DocenteCapacitado
    extra = 1
    max_num = 100
    fields = [
        'fecha_capacitacion', 'area_capacitacion', 'tema',
        'nombres', 'apellidos', 'correo', 'cedula', 'telefono'
    ]



class CustomTableSection(TableSection):
    verbose_name = "Capacitacion docente"  # Displays custom table title
    height = 300  # Force the table height. Ideal for large amount of records
    related_name = "docentes_capacitados"  # Related model field name
    fields = [
        'fecha_capacitacion', 'area_capacitacion', 'tema',
        'nombres', 'apellidos', 'correo', 'cedula', 'telefono'
    ]

    # Custom field
    def custom_field(self, instance):
        return instance.nombres


@admin.register(prospecion_administrativa)
class prospecion_administrativaAdmin(ModelAdmin):
    inlines = [DocenteCapacitadoInline]
    list_sections = [CustomTableSection]  # Agregar la sección personalizada

    # Mostrar campos clave
    list_display = [
        'nombre', 'estado', 'fecha_estado_actualizado',
        'ciudad', 'mail_institucion_general',
        'responsable_institucional_1', 'telefono_responsable_1'
    ]

    list_filter = ['estado', 'sucursal', 'fecha_estado_actualizado']
    search_fields = ['nombre', 'ciudad', 'responsable_institucional_1']

    actions = [export_to_csv, export_to_excel]

    # Mostrar botón cancelar en formularios
    change_form_show_cancel_button = True

    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
        # Si usas campos tipo ArrayField (de PostgreSQL)
        # ArrayField: {"widget": ArrayWidget},
    }

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)

    verbose_name = "Perfil Institución"
    verbose_name_plural = "Perfiles de Instituciones"


@admin.action(description="Duplicar mensajes seleccionados")
def duplicar_mensajes(modeladmin, request, queryset):
    for mensaje in queryset:
        mensaje.pk = None  # Elimina la clave primaria para crear una nueva entrada
        mensaje.fecha_envio = timezone.now()  # Nueva fecha de envío
        mensaje.creado = timezone.now()       # Nueva fecha de creación
        mensaje.task_id = None                # Limpia task_id para evitar referencias repetidas
        mensaje.task_status = "No asignada"   # Reinicia el estado de la tarea
        mensaje.save()

@admin.register(Mensaje)
class MensajeAdmin(ModelAdmin):
    list_display = ['emisor', 'receptor', 'asunto', 'leido', 'fecha_envio']
    list_filter = ['leido', 'asunto', 'sucursal']
    search_fields = ['emisor__username', 'receptor__username', 'cuerpo']
    actions = [duplicar_mensajes]

    list_filter_submit = True  # Submit button at the bottom of the filter
    list_filter = (
        ("fecha_envio", RangeDateTimeFilter),
    )

    def estado_tarea_coloreado(self, obj):
        estado = obj.estado_tarea

        colores = {
            'PENDING': 'gray',
            'RECEIVED': 'gray',
            'STARTED': 'blue',
            'RETRY': 'orange',
            'SUCCESS': 'green',
            'FAILURE': 'red',
        }

        color = colores.get(estado.upper(), 'black')

        return format_html(
            '<span style="padding:2px 6px; background-color:{}; color:white; border-radius:4px;">{}</span>',
            color, estado
        )

    estado_tarea_coloreado.short_description = "Estado de la tarea"
    estado_tarea_coloreado.admin_order_field = 'task_id'


@admin.register(pagos)
class PagosAdmin(ModelAdmin):
    list_display = ['profile', 'cuenta', 'colegio', 'plan','servicio','estado_de_pago','convenio','pago']
    list_filter_sheet = True
    list_filter_submit = True  # Submit button at the bottom of the filter
    actions = [ export_to_csv, export_to_excel]

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
   # change_form_outer_before_template = "some/template.html"
   # change_form_outer_after_template = "some/template.html"

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




#@admin.register(Cita, site=custom_admin_site)
#class CitaAdmin(ModelAdmin):  # Usamos unfold.ModelAdmin



def ver_en_calendario(obj):
    return mark_safe('<a href="{}"><span class="material-symbols-outlined">calendar_month</span>'.format(
        reverse('custom_admin:admin_cita_detail', args=[obj.id])))













DATA = {
    "headers": [
        # Col 1 header
        {
            "title": "Title",
            "subtitle": "something",  # Optional
        },
    ],
    "rows": [
        # First row
        {
            # Row heading
            "header": {
                "title": "Title",
                "subtitle": "something",  # Optional
            },
            "cols": [
                # Col 1 cell value
                {
                    "value": "1",
                    "subtitle": "something",  # Optional
                }
            ]
        },
        # Second row
        {
            # Row heading
            "header": {
                "title": "Title",
                "subtitle": "something",  # Optional
            },
            "cols": [
                # Col 1 cell value
                {
                    "value": "1",
                }
            ]
        },
    ]
}

@register_component
class MyCohortComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "data": DATA
        })
        return context




@register_component
class CitasCohortComponent(BaseComponent):
    template_name = "admin/citas_cohort.html"  # Asegúrate de tener este template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filtramos las citas pendientes
        citas = Cita.objects.filter(fecha__gte=now(), estado='pendiente')

        # Construcción de datos para la tabla
        data = {
            "headers": [
                {"title": "Creador"},
                {"title": "Destinatario"},
                {"title": "Fecha"},
                {"title": "Estado"},
            ],
            "rows": [],
        }

        # Llenar las filas con las citas obtenidas
        for cita in citas:
            row = {
                "header": {
                    "title": f"Cita #{cita.id}",
                    "subtitle": cita.motivo,
                },
                "cols": [
                    {"value": cita.creador.get_full_name() or cita.creador.username},
                    {"value": cita.destinatario.get_full_name() or cita.destinatario.username},
                    {"value": cita.fecha.strftime('%d/%m/%Y %H:%M')},
                    {"value": cita.estado.capitalize()},
                ]
            }
            data["rows"].append(row)

        # Pasamos los datos al contexto
        context["data"] = data
        return context


@admin.register(Sucursal)
class SucursalAdmin(ModelAdmin):
    list_display = ('nombre', 'direccion', 'persona_encargada', 'correo')
    search_fields = ('nombre', 'direccion', 'persona_encargada')



class CardSection(TemplateSection):
    template_name = "admin/test2.html"

class CitasComentariosInline(admin.TabularInline):
    model = ComentarioCita
    extra = 1
    fields = ["autor", "texto", "fecha_creacion"]
    readonly_fields = ('fecha_creacion',)
    show_change_link = False


class ComentariosCitaSection(TableSection):
    verbose_name = "Comentarios de la cita"
    height = 300
    related_name = "comentarios"  # Esto viene del related_name del modelo
    fields = ["autor", "texto", "fecha_creacion"]

    # Custom field
    def custom_field(self, instance):
        return instance.pk



@admin.register(Cita)
class CitaAdmin(ModelAdmin):  # Usamos unfold.ModelAdmin
    list_sections = [CardSection,ComentariosCitaSection]
    list_per_page = 20


    list_display = ("creador", "destinatario", "fecha", "estado", "motivo", ver_en_calendario)
    search_fields = ("motivo", "notas", "creador__username", "destinatario__username")
    list_filter = ("estado", "fecha")
    actions = [ export_to_csv, export_to_excel]
    
   # change_list_template = "admin/dashboard_calendar.html"  # Cambia la plantilla de la lista de cambios


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
    list_fullwidth = True

    # Set to False, to enable filter as "sidebar"
    list_filter_sheet = True

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = True

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
   # change_form_outer_before_template = "some/template.html"
   # change_form_outer_after_template = "some/template.html"

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
    def ver_en_calendario(self, obj):
        return ver_en_calendario(obj)
    ver_en_calendario.short_description = "Calendario"
    ver_en_calendario.allow_tags = True

    #list_sections = [CardSection]


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')



class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'frequency')
    search_fields = ('name',)



class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end', 'calendar', 'creator')
    list_filter = ('calendar',)
    search_fields = ('title', 'description')



class OccurrenceAdmin(admin.ModelAdmin):
    list_display = ('event', 'start', 'end', 'cancelled')
    list_filter = ('cancelled',)
    search_fields = ('event__title',)


class PagosItemInline(admin.TabularInline):
    model = pagos
    raw_id_fields = ['cliente']
    readonly_fields = ['cuenta', 'sucursal', 'colegio', 'plan', 'convenio', 'servicio', 'estado_de_pago']
    fields = ['cuenta', 'sucursal', 'colegio', 'estado_de_pago']  # Solo mostramos estos 4 campos
    can_delete = False
    extra = 0
    max_num = 0  # Evita que se agreguen nuevos elementos

class TareaItemInline(admin.TabularInline):
    model = tareas
    raw_id_fields = ['paciente']
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
    readonly_fields = ['edad']  
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

    list_display = ['nombre_paciente', 'apellidos_paciente','edad','institucion','celular','tipo_servicio','fecha_inicio','fecha_terminacion']
    list_filter= ['nombre_paciente','sucursales','tipo_servicio','fecha_inicio','fecha_terminacion']
    actions = [ export_to_csv, export_to_excel]
    verbose_name = "Registro Administrativo / Ingreso de Paciente"
    verbose_name_plural = "Registro Administrativo / Ingreso de Paciente"    
   #inlines = [MensajesEnviadosInline, MensajesRecibidosInline]

    fieldsets = (
        ('Ingresar Información Personal del Paciente', {
            'fields': ('user','sucursales', 'photo', 'ruc','nombre_paciente','apellidos_paciente','nacionalidad','sexo','fecha_nacimiento','edad','unidad_educativa'),
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

    


