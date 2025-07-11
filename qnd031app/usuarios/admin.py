import csv
import xlsxwriter
from django.contrib import admin
from django.http import HttpResponse
from .models import Profile, BitacoraDesarrollo, Perfil_Terapeuta, Mensaje, Sucursal , ValoracionTerapia ,DocenteCapacitado, Cita,ComentarioCita, TareaComentario ,AsistenciaTerapeuta,prospecion_administrativa,Prospeccion, tareas, pagos
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
#from schedule.models import Calendar, Event, Rule, Occurrence
#from schedule.admin import CalendarAdmin 
from django.utils.timezone import localtime
from django.utils.timezone import make_aware
from django import forms
from django.utils import timezone
from unfold.components import BaseComponent, register_component
from unfold.sections import TableSection, TemplateSection
from django.utils.timezone import now
from .forms import  CitaForm,AdministrativeProfileForm, AsistenciaTerapeutaAdminForm,CitaAdminForm, ValoracionTerapiaAdminForm, ProfileAdminForm, PerfilTerapeutaAdminForm,PerfilTerapeutaForm, ServicioTerapeuticoForm, ProspecionAdministrativaForm,PerfilTerapeutaForm,PerfilPacientesForm
from django.template.loader import render_to_string
from unfold.decorators import action
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.html import format_html
from unfold.admin import StackedInline, TabularInline
from serviceapp.models import ServicioTerapeutico

from unfold.contrib.filters.admin import (
    AutocompleteSelectFilter,
    AutocompleteSelectMultipleFilter,
     RangeDateFilter, RangeDateTimeFilter
)
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .widgets import CustomDatePickerWidget
from .models import AdministrativeProfile
from django.contrib.auth.admin import UserAdmin

from collections import defaultdict
from django.template.loader import render_to_string
from django.utils import timezone
from collections import defaultdict
from django.utils.timezone import localtime, is_naive, make_aware
from datetime import timedelta, time, date
from datetime import datetime
from django.contrib.auth import get_user_model




def dashboard_callback(request, context):
    context.update({
        "users_count": get_user_model().objects.count(),
        "orders_count": Profile.objects.count(),
    })
    return context



# 1. Anular el registro por defecto
#admin.site.unregister(User)
admin.site.unregister(Group)




# Registrar el modelo Group con estilo Unfold también
@admin.register(Group)
class CustomGroupAdmin(GroupAdmin, ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)




@admin.register(Sucursal)
class SucursalAdmin(ModelAdmin):
    list_display = ('nombre', 'direccion', 'persona_encargada', 'correo')
    search_fields = ('nombre', 'direccion', 'persona_encargada')




class CitasComentariosInline(admin.TabularInline):
    model = Cita
    extra = 1
    fields = ["notas",]
    readonly_fields = ('fecha',)
    show_change_link = False


class ComentariosCitaSection(TableSection):
    verbose_name = "Comentarios de la cita"
    height = 300
    fields = ["notas"] 
    
    # Custom field
    def custom_field(self, instance):
        return instance.pk
    def render(self):
        return render_to_string("admin/test2.html", {"instance": self.instance})





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
            if isinstance(value, datetime): 
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
            if isinstance(value, datetime):
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



@register_component
class ValoracionComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Valoracion"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        p = self.instance  # Solo la instancia actual

        headers = [
            "Edad",'servicio', "Institución",    
            'fecha de asesoria','Valoracion/Archivo Adjunto'
        ]

        row = [
            p.edad,
            p.servicio,
            p.institucion if p.institucion else "",
            p.fecha_asesoria.strftime('%d/%m/%Y') if p.fecha_asesoria else "Sin Fecha de Asesoría",
            p.archivo_adjunto.url if p.archivo_adjunto else "Sin Archivo Adjunto",
        ]

        context.update({
            "title": f"Información de Valoración",
            "table": {
                "headers": headers,
                "rows": [row],  # Solo una fila con la instancia actual
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())

@register_component
class ValoracionExtraComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Información DECE"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        v = self.instance  # Instancia actual de ValoracionTerapia

        headers = [
            "Observaciones",
        ]

        row = [
            v.observaciones if v.observaciones else "Sin observaciones",
        ]

        context.update({
            "title": "Información Complementaria de Valoración",
            "table": {
                "headers": headers,
                "rows": [row],
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())

@admin.register(ValoracionTerapia)
class ValoracionTerapiaAdmin(ModelAdmin):
    form= ValoracionTerapiaAdminForm
    list_display = ['get_perfil_terapeuta_full_name','nombre', 'fecha_valoracion','recibe_asesoria','necesita_terapia','toma_terapia', 'proceso_terapia' ]
    exclude = ('perfil_terapeuta',)
    search_fields = ['nombre', 'perfil_terapeuta__first_name', 'perfil_terapeuta__last_name']
    list_editable = ['proceso_terapia', 'recibe_asesoria','necesita_terapia','toma_terapia' ]
    readonly_fields = ['edad']
    list_sections = [ValoracionComponent,ValoracionExtraComponent]
    #exclude = ('edad',)
    list_filter = ("sucursal",'recibe_asesoria', 'proceso_terapia','es_particular','es_convenio')
    order_by = ('-fecha_valoracion',)
    actions = [export_to_csv, export_to_excel]



    def get_perfil_terapeuta_full_name(self, obj):
        return obj.perfil_terapeuta.get_full_name() if obj.perfil_terapeuta else "—"
    get_perfil_terapeuta_full_name.short_description = "Terapeuta a Cargo"
    get_perfil_terapeuta_full_name.admin_order_field = 'perfil_terapeuta__first_name'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.perfil_terapeuta = request.user
        super().save_model(request, obj, form, change)
    



from django.contrib.admin.filters import ChoicesFieldListFilter

class HorizontalChoicesFieldListFilter(ChoicesFieldListFilter):
    horizontal = True # Enable horizontal layout



def badge_callback(request):
    return Perfil_Terapeuta.objects.count()


@register_component
class TerapeutaComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Información Personal"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        p = self.instance  # Solo la instancia actual

        headers = [
            "Nombres Completos","Fecha de Ingreso","edad", "Sexo", 
        ]

        row = [
            p.user.first_name + " " + p.user.last_name,
            p.fecha_ingreso, 
            p.edad,
            p.sexo,
            
            
        ]

        context.update({
            "title": f"Información Personaal",
            "table": {
                "headers": headers,
                "rows": [row],  # Solo una fila con la instancia actual
            }
        })
        return context
    


    def render(self):
        return render_to_string(self.template_name, self.get_context_data())



@register_component
class TerapeutaContactoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Información de Contacto"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        p = self.instance  # Solo la instancia actual

        headers = [
            "Correo Electrónico","Telefono de Contacto","Sucursal-MEDDES®"
        ]

        row = [
            p.correo,
            p.telefonos_contacto,
            p.sucursal,
            
        ]

        context.update({
            "title": f"Información  de Contacto",
            "table": {
                "headers": headers,
                "rows": [row],  # Solo una fila con la instancia actual
            }
        })
        return context
    


    def render(self):
        return render_to_string(self.template_name, self.get_context_data())



@register_component
class TerapeutaBancariaComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Información Bancaria"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        p = self.instance  # Solo la instancia actual

        headers = [
         "Banco", "Cédula", "Tipo de Cuenta", "Número de Cuenta", "Costo Serivicio por Hora"
        ]

        row = [
            p.banco,
            p.cedula,
            p.tipo_cuenta,
            p.numero_cuenta,
            p.pago_por_hora
          
        ]

        context.update({
            "title": f"Información Bancaria",
            "table": {
                "headers": headers,
                "rows": [row],  # Solo una fila con la instancia actual
            }
        })
        return context
    


    def render(self):
        return render_to_string(self.template_name, self.get_context_data())

@admin.register(Perfil_Terapeuta)
class Perfil_TerapeutaAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_sheet = True
    list_fullwidth = False
    list_horizontal_scrollbar_top = False
    list_disable_select_all = False
    change_form_show_cancel_button = True

    list_sections = [
        TerapeutaComponent,
        TerapeutaContactoComponent,
        TerapeutaBancariaComponent
    ]

    list_display = [
        'get_full_name', 'especialidad', 'activo', 
        'servicio_domicilio', 'servicio_institucion','servicio_consulta'
    ]
    list_editable = ['activo', 'servicio_domicilio', 'servicio_institucion', 'servicio_consulta']

    list_filter = [
        'sucursal',
        'activo',
        'servicio_institucion',
        'servicio_domicilio',
    ]

    search_fields = (
        'user__first_name', 
        'user__last_name',
        'nombres_completos',
        'correo',
        'sucursal__nombre',  # Asegúrate de que 'nombre' esté en Sucursal
    )

    form = PerfilTerapeutaAdminForm  # Preferible usar un solo form coherente

    actions = [export_to_csv, export_to_excel]

    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={'rows': 4, 'cols': 60}),
        },
    }

    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",  # Este campo debería existir
        "other_field_name": lambda content: content.strip(),  # Igual, verificar que existan
    }

    def get_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else "Sin usuario"
    get_full_name.short_description = 'Terapeuta Registrado'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)



@register_component
class AsistenciaComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Información Asistencia terapeuta"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance  # instancia de AsistenciaTerapeuta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if hasattr(self.instance, 'terapeuta'):
            terapeuta = self.instance.terapeuta
        else:
            terapeuta = self.instance  # fallback (por si se pasa directamente un User)

        if not isinstance(terapeuta, User):
            context.update({"error": "Instancia no válida para el componente."})
            return context

        asistencias = AsistenciaTerapeuta.objects.filter(terapeuta=terapeuta)

        headers = [
            "Evento", "Sucursal", "Hora de salida", "¿Asistirá?", "¿No asistirá?", "Observaciones"
        ]

        rows = []
        for asistencia in asistencias:
            rows.append([
                str(asistencia.evento) if asistencia.evento else "Sin evento",
                str(asistencia.sucursal) if asistencia.sucursal else "Sin sucursal",
                asistencia.hora_salida.strftime("%H:%M") if asistencia.hora_salida else "Sin hora",
                "✅" if asistencia.asistire else "❌",
                "✅" if asistencia.no_asistire else "❌",
                asistencia.observaciones or "Sin observaciones"
            ])

        context.update({
            "title": f"Asistencia de {terapeuta.get_full_name() if terapeuta else '—'}",
            "table": {
                "headers": headers,
                "rows": rows,
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())








@admin.register(AsistenciaTerapeuta)
class AsistenciaTerapeutaAdmin(ModelAdmin):
    change_form_show_cancel_button = True
    form = AsistenciaTerapeutaAdminForm

    list_display = ('get_terapeuta_full_name', 'evento', 'hora_salida', 'no_asistire', 'asistire')
    list_filter = ('terapeuta', 'no_asistire', 'asistire', 'evento')
    list_sections = [AsistenciaComponent]
    list_editable = ('no_asistire', 'asistire')
    search_fields = ('terapeuta__first_name', 'terapeuta__last_name')
    autocomplete_fields = ['terapeuta']
    actions = [export_to_csv, export_to_excel]
    exclude = ('terapeuta',)



    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        # Filtrar asistencias donde el evento tiene como profile_terapeuta al usuario actual
        return qs.filter(evento__profile_terapeuta__user=request.user)

    def get_terapeuta_full_name(self, obj):
        if obj.terapeuta:
            return f"{obj.terapeuta.first_name} {obj.terapeuta.last_name}".strip()
        return "—"
    get_terapeuta_full_name.short_description = "Terapeuta a Cargo"
    get_terapeuta_full_name.admin_order_field = 'terapeuta__first_name'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.terapeuta = request.user
        super().save_model(request, obj, form, change)




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
    list_fullwidth = True
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
        'minutos_restantes',
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
    readonly_fields = ('fecha', 'fecha_entrega')

    # Overrides para campos especiales
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    }


    

class TareasComentariosInline(TabularInline):
    model = TareaComentario
    extra = 1
    fields = ('tarea', 'mensaje', 'archivo', 'fecha')
    readonly_fields = ('fecha',)
    show_change_link = False
    tab = True
    


@register_component
class TareasComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Actividades"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance  # Puede ser Profile o tareas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Determinar si la instancia es Profile o tareas
        if isinstance(self.instance, Profile):
            profile = self.instance
        elif isinstance(self.instance, tareas):
            profile = self.instance.profile
        else:
            profile = None

        if profile is None:
            context.update({
                "title": "Tareas asignadas",
                "table": {
                    "headers": ["Sin datos disponibles"],
                    "rows": [["No se pudo obtener un perfil válido."]],
                }
            })
            return context

        tareas_asignadas = tareas.objects.filter(profile=profile)

        headers = [
            "Título", "Fecha de envío", "Fecha de entrega",
            "¿Realizada?", "¿Culminó terapia?", "Archivo adjunto", "Multimedia"
        ]

        rows = []
        for tarea in tareas_asignadas:
            rows.append([
                tarea.titulo or "Sin título",
                tarea.fecha_envio.strftime("%d/%m/%Y") if tarea.fecha_envio else "Sin fecha",
                tarea.fecha_entrega.strftime("%d/%m/%Y") if tarea.fecha_entrega else "Sin fecha",
                "✅" if tarea.realizada else "❌",
                "✅" if tarea.tarea_no_realizada else "❌",
                tarea.material_adjunto.url if tarea.material_adjunto else "N/A",
                tarea.media_terapia.url if tarea.media_terapia else "N/A",
            ])

        context.update({
            "title": f"Tareas asignadas a {profile.nombre_completo}",
            "table": {
                "headers": headers,
                "rows": rows,
            }
        })

        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())

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



    search_fields = ['profile__nombre_completo', 'terapeuta__nombres_completos', 'tarea']
    list_filter = (
        'fecha_envio',
        'fecha_entrega',)
    list_editable = ['asistire',]
    list_sections = [TareasComponent]

    list_display = ['get_terapeuta_full_name','profile', 'fecha_envio','fecha_entrega', 'asistire',]
    exclude = ('terapeuta',)
    actions = [ export_to_csv, export_to_excel]
    verbose_name = "Registro Administrativo / Tarea Terapéutica"
    verbose_name_plural = "Administrativo / Tareas Terapéuticas"

    def get_terapeuta_full_name(self, obj):
        return obj.terapeuta.get_full_name() if obj.terapeuta else "—"
    get_terapeuta_full_name.short_description = "Terapeuta a Cargo"
    get_terapeuta_full_name.admin_order_field = 'terapeuta__first_name'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.terapeuta = request.user
        super().save_model(request, obj, form, change)



@register_component
class ProspeccionComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Prospección"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        p = self.instance  # Instancia actual de Prospeccion

        headers = [
            "Provincia",
            "Nombre de la Institución",
            "Estado",
            "Teléfono",
            "Dirección",
            "Nombre de Contacto",
            "Cargo del Contacto",
            "Email de Contacto",
            "Proceso Realizado",
            "Responsable del contacto",
            "Fecha de Contacto",
            "Observaciones",
            "Fecha Próximo Contacto",
        ]

        row = [
            p.provincia,
            p.nombre_institucion,
            p.estado,
            p.telefono or "",
            p.direccion or "",
            p.nombre_contacto or "",
            p.cargo_contacto or "",
            p.email_contacto or "",
            p.proceso_realizado or "",
            p.responsable or "",
            p.fecha_contacto or "",
            p.observaciones or "",
            p.fecha_proximo_contacto or "",
        ]

        context.update({
            "title": f"Información de Prospección",
            "table": {
                "headers": headers,
                "rows": [row],  # Solo una fila con la instancia actual
            }
        })

        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())



@admin.register(Prospeccion)
class ProspeccionAdmin(ModelAdmin):
    # Campos comprimidos en el formulario
    compressed_fields = True

    # Advertencia de cambios no guardados
    warn_unsaved_form = True

    # Procesamiento previo de campos de solo lectura
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }

    # Ocultar botón de envío en filtros
    list_filter_submit = False

    # Listado no en modo full width
    list_fullwidth = False

    # Filtros como hoja lateral (no sidebar)
    list_filter_sheet = True

    # No mostrar scrollbar arriba en el listado
    list_horizontal_scrollbar_top = False

    # No seleccionar todos por defecto
    list_disable_select_all = False

    # Desactivar acciones
    actions_list = []
    actions_row = []
    actions_detail = []
    actions_submit_line = []

    # Mostrar botón de cancelar
    change_form_show_cancel_button = True

    # Personaliza los widgets de campos
    formfield_overrides = {
        models.TextField: {
            "widget": admin.widgets.AdminTextareaWidget(attrs={'rows': 3}),
        },
    }

    # Campos que se muestran en la lista del admin
    list_display = [
        'nombre_institucion',
        'provincia',
        'estado',
        'telefono',
        'responsable',
        'fecha_contacto',
        'fecha_proximo_contacto',
    ]

    # Campos que se pueden buscar
    search_fields = [
        'nombre_institucion',
        'provincia',
        'estado',
        'nombre_contacto',
        'email_contacto',
        'responsable__first_name',
        'responsable__last_name',
    ]

    # Filtros laterales
    list_filter = [
        'provincia',
        'estado',
        'responsable',
        'fecha_contacto',
        'fecha_proximo_contacto',
    ]

    list_sections = [ProspeccionComponent]  # Agregar la sección personalizada

    # Orden predeterminado
    ordering = ['-fecha_contacto']

    # Etiquetas personalizadas para el admin
    verbose_name = "Administrativo / Prospecciones"
    verbose_name_plural = "Registros Administrativos / Prospección"

class DocenteCapacitadoInline(TabularInline):
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
    conditional_fields = {
        "fecha_activo": "es_activo == true",
    }
    inlines = [DocenteCapacitadoInline]
    list_sections = [CustomTableSection]  # Agregar la sección personalizada

    # Mostrar campos clave
    list_display = [
        'nombre','responsable_institucional_1','mail_responsable_1','telefono_responsable_1', 'es_en_cita','es_convenio_firmado', 'es_valoracion','es_inactivo', 'es_finalizado'
    ]
    #list_editable = ('pendiente','confirmada','cancelada',)
    list_filter = (
        'sucursal',  # Filtro por sucursal
        'es_en_cita', 'es_valoracion', 'es_finalizado',
        
       
    )
    list_editable = ['es_en_cita','es_convenio_firmado','es_inactivo', 'es_valoracion', 'es_finalizado']

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

@admin.action(description="Duplicar citas seleccionadas")
def duplicar_citas(modeladmin, request, queryset):
    for cita in queryset:
        cita.pk = None  # Elimina la clave primaria
        cita.fecha = timezone.now()  # O puedes hacer cita.fecha + timedelta
        cita.fecha_final = None  # Opcionalmente limpiar
       # cita.estado = 'pendiente'  # Estado reiniciado
        cita.is_active = False  # Estado paciente
        cita.is_deleted = False  # No cancelada
        cita.save()


@register_component
class MensajeComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Mensaje"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance  # instancia de Mensaje

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        m = self.instance

        headers = [
            "Receptor", "Asunto", "Leído", "Sucursal", "Cuerpo"
        ]

        row = [
            str(m.receptor) if m.receptor else "Desconocido",
            m.get_asunto_display() if m.asunto else "Sin asunto",
            "Sí" if m.leido else "No",
            str(m.sucursal) if m.sucursal else "Sin sucursal",
            m.cuerpo or "Sin contenido",
        ]

        context.update({
            "title": f"Información del Mensaje",
            "table": {
                "headers": headers,
                "rows": [row],
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())

@admin.register(Mensaje)
class MensajeAdmin(ModelAdmin):
    list_display = ['get_emisor_full_name', 'get_receptor_full_name', 'asunto', 'fecha_envio', 'leido']
    list_filter = ['leido', 'asunto', 'sucursal']
    list_sections = [MensajeComponent]
    exclude= ('emisor','creado')
    list_editable = ['leido']
    search_fields = ['emisor__username', 'receptor__username', 'cuerpo']
    actions = [duplicar_mensajes]

    list_filter_submit = True  # Submit button at the bottom of the filter
    list_filter = (
        ("fecha_envio", RangeDateTimeFilter),
    )

    def get_emisor_full_name(self, obj):
        return obj.emisor.get_full_name() if obj.emisor else "—"
    get_emisor_full_name.short_description = "Desde"
    get_emisor_full_name.admin_order_field = 'emisor__first_name'

    def get_receptor_full_name(self, obj):
        return obj.receptor.get_full_name() if obj.receptor else "—"
    get_receptor_full_name.short_description = "Para"
    get_emisor_full_name.admin_order_field = 'receptor__first_name'           

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.emisor = request.user
        super().save_model(request, obj, form, change)
    

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


@register_component
class PagosComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Información de Cuenta"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        p = self.instance  # Solo la instancia actual

        headers = [
        "Nombre de Paciente","sucursal-MEDDES®",
        ]

        row = [
            p.profile.nombre_paciente + " " + p.profile.apellidos_paciente,
            p.sucursal,
        ]

        context.update({
            "title": f"Orden de pago paciente: {p.profile.nombre_paciente} {p.profile.apellidos_paciente}",
            "table": {
                "headers": headers,
                "rows": [row],  # Solo una fila con la instancia actual
            }
        })
        return context
    


    def render(self):
        return render_to_string(self.template_name, self.get_context_data())

@admin.register(pagos)
class PagosAdmin(ModelAdmin):
    list_display = ['numero_factura','pago','vencido','pendiente','al_dia']
    list_editable = ['vencido','pendiente','al_dia',]
    list_sections = [PagosComponent]
    list_filter = ('sucursal',"vencido",'pendiente','al_dia')
    search_fields = ('numero_factura',)
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




@register_component
class CitasCohortComponent(BaseComponent):
    template_name = "admin/test.html"

    def __init__(self, request, instance=None):
        super().__init__(request)
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cita_centrada = self.instance
        if not cita_centrada or not cita_centrada.fecha:
            base_date = localtime(make_aware(datetime.now())).date()
        else:
            base_date = cita_centrada.fecha

        # Mostrar 2 días antes y 2 días después (lunes a domingo)
        start_date = base_date - timedelta(days=2)
        end_date = base_date + timedelta(days=2)

        # Cambiado a 7:00 a 22:00
        time_slots = [time(hour=h) for h in range(7, 23)]

        agenda = defaultdict(lambda: defaultdict(list))
        fechas_unicas = set()
        horas_unicas = set()

        for i in range((end_date - start_date).days + 1):
            dia = start_date + timedelta(days=i)

            dia_str = dia.strftime("%Y-%m-%d")
            fechas_unicas.add(dia_str)

            for t in time_slots:
                hora_str = t.strftime("%H:%M")
                agenda[dia_str][hora_str]
                horas_unicas.add(hora_str)

        # Filtrado ajustado a nueva franja horaria
        citas = Cita.objects.filter(
            fecha__range=(start_date, end_date),
            hora__range=(time(7, 0), time(22, 0))
        ).select_related("creador", "destinatario")

        for cita in citas:
            if not cita.fecha or not cita.hora:
                continue

            cita_dt = datetime.combine(cita.fecha, cita.hora)
            if is_naive(cita_dt):
                cita_dt = make_aware(cita_dt)
            cita_dt = localtime(cita_dt)

            dia_str = cita_dt.strftime("%Y-%m-%d")
            hora_str = cita_dt.strftime("%H:%M")

            agenda[dia_str][hora_str].append({
                "id": cita.id,
                "motivo": cita.motivo or "Sin motivo",
                "creador": cita.creador.get_full_name() if cita.creador else "Sin creador",
                "destinatario": cita.destinatario.get_full_name() if cita.destinatario else "Sin destinatario",
                "estado": (
                    "Confirmada" if cita.confirmada
                    else "Pendiente" if cita.pendiente
                    else "Cancelada"
                ),
                "tipo_cita": cita.tipo_cita or "sin_tipo",
                "hora": hora_str,
            })

        dias_date = [datetime.strptime(d, "%Y-%m-%d").date() for d in fechas_unicas]

        agenda_dias = []
        for d in sorted(dias_date):
            d_str = d.strftime("%Y-%m-%d")
            agenda_dias.append({
                "date": d,
                "str": d_str,
                "agenda": agenda[d_str],
            })

        context["agenda_dias"] = agenda_dias
        context["horas"] = sorted(horas_unicas)

        return context

    def render(self):
        context = self.get_context_data()
        return render_to_string(self.template_name, context, request=self.request)

        

class CardSection(TemplateSection):
    template_name = "admin/test2.html"



from .widgets import CustomDatePickerWidget, CustomTimePickerWidget
# Asegúrate de importar: export_to_csv, export_to_excel, duplicar_citas, WysiwygWidget, ArrayWidget
@admin.register(Cita)
class CitaAdmin(ModelAdmin):
    form = CitaForm  # Asegúrate de que CitaForm esté definido en tu forms.py
    #form = CitaForm 
    formfield_overrides = {
        models.DateField: {'widget': CustomDatePickerWidget()},
        models.TimeField: {'widget': CustomTimePickerWidget()},
    }

    list_sections = [ComentariosCitaSection, CitasCohortComponent]
    list_sections_layout = "horizontal"
    
    conditional_fields = {
    # Campos exclusivos de tipo 'terapeutica'
    "profile": "tipo_cita == 'terapeutica'",
    "perfil_terapeuta": "tipo_cita == 'terapeutica'",

    # Campos exclusivos de tipo 'particular'
    "nombre_paciente": "tipo_cita == 'particular'",

    # Campos compartidos entre 'administrativa' y 'particular'
    "destinatario": "tipo_cita == 'administrativa' ",

    # Campos comunes a todos los tipos
    "fecha": "tipo_cita == 'terapeutica' or tipo_cita == 'administrativa' or tipo_cita == 'particular'",
    "hora": "tipo_cita == 'terapeutica' or tipo_cita == 'administrativa' or tipo_cita == 'particular'",
    "motivo": "tipo_cita == 'terapeutica' or tipo_cita == 'administrativa' or tipo_cita == 'particular'",
    "notas": "tipo_cita == 'terapeutica' or tipo_cita == 'administrativa' or tipo_cita == 'particular'",
    }

    list_per_page = 20
    compressed_fields = True
    list_horizontal_scrollbar_top = True
    list_display = (
        "get_destinatario_full_name", "tipo_cita", "fecha", 'hora', "motivo",
        'pendiente', 'cancelada', 'confirmada'
    )
    list_editable = ('pendiente', 'confirmada', 'cancelada',)
    search_fields = (
        "motivo", "notas", "creador__first_name", "destinatario__first_name",
    )
    list_filter = ('sucursal', 'pendiente', 'confirmada', 'cancelada', "fecha",)
    change_form_show_cancel_button = True
    exclude = ('creador',)
    ordering = ['fecha']

    actions = [export_to_csv, export_to_excel, duplicar_citas]
    actions_list = []
    actions_row = []
    actions_submit_line = []

    def get_destinatario_full_name(self, obj):
        return obj.destinatario.get_full_name() if obj.destinatario else "—"
    get_destinatario_full_name.short_description = "Cita para"
    get_destinatario_full_name.admin_order_field = 'destinatario__first_name'

    def get_admin_changelist_url(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return reverse_lazy(f"admin:{app_label}_{model_name}_changelist")

    @action
    def changelist_action(self, request: HttpRequest, object_id=None):
        url = self.get_admin_changelist_url()
        return redirect(url)

    changelist_action.short_description = "Volver a Registros"
    actions_detail = ["changelist_action"]

    def has_changelist_action_permission(self, request, object_id=None):
        return True

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creador = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="Calendario")
    def ver_en_calendario(self, obj):
        return format_html('<a href="{}">Ver</a>', obj.get_calendar_url())

        # Override sólo el campo dias_recurrentes para que use checkbox múltiple

    








class OccurrenceAdmin(admin.ModelAdmin):
    list_display = ('event', 'start', 'end', 'cancelled')
    list_filter = ('cancelled',)
    search_fields = ('event__title',)


class PagosItemInline(TabularInline):
    model = pagos
    raw_id_fields = ['profile']
    readonly_fields = ['numero_factura', 'sucursal']
    fields = ['numero_factura', 'sucursal', 'al_dia','pendiente','vencido']  # Solo mostramos estos 4 campos
    can_delete = False
    extra = 0
    max_num = 0  # Evita que se agreguen nuevos elementos
    tab = True

class TareaItemInline(TabularInline):
    model = tareas
    raw_id_fields = ['profile']
    readonly_fields = [ 'titulo', 'terapeuta', 'fecha_envio', 'descripcion_tarea']
    fields = ['titulo', 'terapeuta', 'fecha_envio', 'descripcion_tarea','media_terapia']  # Mostramos solo estos 4 campos
    can_delete = True
    extra = 0
    max_num = 0
    tab = True

class CitaItemInline(TabularInline):
    model = Cita
    raw_id_fields = ['creador']
    readonly_fields = ['creador', 'destinatario', 'motivo', 'fecha']
    fields = ['creador', 'fecha', 'motivo', ]  # Mostramos solo estos 4 campos
    can_delete = False
    extra = 0
    max_num = 0
    tab = True





class DatosTerapiaSection(TableSection):
    verbose_name = "🧠 Datos Terapéuticos"
    height = 400
    fields = [
        "es_en_terapia",
        "es_pausa",
        "es_retirado",
        "es_alta",
        "tipo_servicio",
        "valorizacion_terapeutica",
        "certificado_inicio",
        "certificado_final",
        "fecha_inicio",
        "fecha_alta",
        "fecha_retiro",
        "motivo_retiro",
        "motivo_otro",
        "fecha_pausa",
        "fecha_re_inicio",
    ]


@register_component
class ProfileComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Perfil de Paciente"

    def __init__(self, request, instance=None):
        super().__init__(request)  # Corrección importante
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = {}  # No dependemos de super()

        p = self.instance  # Instancia del perfil

        headers = [
            "Foto", "Nombre Completo", "Edad", "Sexo", "Institución", "Teléfono",
        ]

        row = [
            format_html('<img src="{}" style="width:80px; border-radius:50%;" />', p.photo.url) if p.photo else "Sin foto",
            f"{p.user.first_name} {p.user.last_name}" if p.user else "Sin usuario",
            p.edad_detallada if hasattr(p, "edad_detallada") else p.edad or "Desconocida",
            p.sexo or "No especificado",
            str(p.institucion) if p.institucion else "N/A",
            str(p.telefono) if p.telefono else "N/A",
        ]

        context.update({
            "title": "Información personal del paciente",
            "table": {
                "headers": headers,
                "rows": [row],
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data(), request=self.request)


@register_component
class ProfileComponentRepresentante(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Perfil de Representante Legal"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        p = self.instance  # Solo la instancia actual

        headers = [
            "Representante","Correo Electrónico",
            "Teléfono", "Celular", "Dirección", "Relación",
        ]

        row = [
            f"{p.nombres_representante_legal} {p.apellidos_representante_legal}",
            p.email,
            p.telefono,
            p.celular,
            p.direccion,
            p.relacion_del_representante,    
        ]

        context.update({
            "title": f"Información del Representante",
            "table": {
                "headers": headers,
                "rows": [row],  # Solo una fila con la instancia actual
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


@register_component
class ProfileComponentTerapeutico(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Perfil de Representante Legal"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        p = self.instance  # Instancia actual

        # Renderizar los terapeutas como una lista de nombres
        terapeutas = ", ".join([
            str(t.user.get_full_name()) if t.user else "Sin usuario"
            for t in p.user_terapeutas.all()
        ]) or "Sin terapeutas asignados"

        headers = [
            "Terapeuta Asignado", "Valorización Terapéutica",
            "Tipo de Servicio", "Certificado de Inicio",
            "Fecha de Retiro", "Fecha de Pausa",
        ]

        row = [
            terapeutas,
            p.valorizacion_terapeutica,
            ", ".join(p.tipos or []) if p.tipos else "Sin tipos",
            format_html('<a href="{}" target="_blank">Ver certificado</a>', p.certificado_inicio.url)
                if p.certificado_inicio else "Sin aprobación",
            p.fecha_retiro or "—",
            p.fecha_pausa or "—",
        ]

        context.update({
            "title": "Información Terapéutica",
            "table": {
                "headers": headers,
                "rows": [row],
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())




@register_component
class ProfileComponentInformes(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Perfil de Representante Legal"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        p = self.instance  # Solo la instancia actual

        headers = [
            "Autorización de inicio","Informe inicial",
            "Informe de seguimiento 3 meses", "Informe de seguimiento 6 meses",
            "Certificado de Alta"
        ]

        row = [
            p.certificado_inicio,
            p.informe_inicial,
            p.informe_segimiento ,
            p.informe_segimiento_2,
            p.certificado_final,
        ]

        context.update({
            "title": f"Información Terapéutica",
            "table": {
                "headers": headers,
                "rows": [row],  # Solo una fila con la instancia actual
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())


class ProfileCardSection(TemplateSection):
    model = Profile
    template_name = "admin/profile_card.html"
    verbose_name = "Perfil"





@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    autocomplete_fields = ['user','sucursales']
            # Display fields in changeform in compressed mode
    compressed_fields = True  # Default: False
    inlines = [TareaItemInline,CitaItemInline,PagosItemInline,]
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    list_sections = [ProfileComponent,ProfileComponentRepresentante,ProfileComponentTerapeutico,ProfileComponentInformes]  # Agregar sección personalizada
    form = ProfileAdminForm
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
    models.DateField: {
        "widget": CustomDatePickerWidget(),  # ← Paréntesis: instancia
    },
}

    list_display = ['get_full_name','fecha_inicio','fecha_alta','es_retirado','es_en_terapia','es_pausa', 'es_alta']

    @admin.display(description='Paciente')
    def get_full_name(self, obj):
        return obj.user.get_full_name()



    list_editable  = ['es_retirado','es_en_terapia','es_pausa', 'es_alta']
    list_filter= ['sucursales','es_retirado','es_en_terapia', 'es_alta',
     ('fecha_inicio', RangeDateFilter), 
     ('fecha_alta', RangeDateFilter), 
    ]
    actions = [ export_to_csv, export_to_excel]
    verbose_name = "Registro Administrativo / Ingreso de Paciente"
    verbose_name_plural = "Registro Administrativo / Ingreso de Paciente"    
   #inlines = [MensajesEnviadosInline, MensajesRecibidosInline]

    fieldsets = (
    ('Ingresar Información Personal del Paciente', {
        'fields': (
            'user',
            'contrasena',
            'sucursales',
            'photo',
            'ruc',
            'nombre_paciente',
            'apellidos_paciente',
            'nacionalidad',
            'sexo',
            'fecha_nacimiento',
            'institucion',
        ),
        'classes': ('collapse',),
    }),
    ('Ingresar Información del Representante Legal', {
        'fields': (
            'nombres_representante_legal',
            'apellidos_representante_legal',
            'relacion_del_representante',
            'nacionalidad_representante',
            'ruc_representante',
            'actividad_economica',
            'email',
            'telefono',
            'celular',
            'provincia',
            'direccion',
        ),
        'classes': ('collapse',),
    }),
    ('Ingresar Información Terapéutica', {
        'fields': (
            'valorizacion_terapeutica',
            'user_terapeutas',            
            'tipos',
            'fecha_inicio',
            'fecha_pausa',
            'fecha_re_inicio',            
            'fecha_alta',
            'certificado_inicio',
            'informe_inicial',
            'informe_segimiento',
            'informe_segimiento_2',
            'certificado_final',

            # Campos booleanos de estados terapéuticos
            'es_en_terapia',
            'es_retirado',
            'es_alta',
            'es_pausa',
        ),
        'classes': ('collapse',),
    }),
)




@register_component
class PerfilAdministrativoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Perfil Administrativo"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        p = self.instance  # instancia actual de AdministrativeProfile

        headers = [
            "Nombre", "Edad (años)",
            "Fecha de ingreso", "Contrato",
            "Pacientes captados", "Valor por paciente",
            "Comisión calculada",
        ]

        row = [
            f"{p.user.first_name} {p.user.last_name}",
            p.age,
            p.date_joined.strftime('%d/%m/%Y') if p.date_joined else "Sin fecha",
            dict(p.contract_type_choices).get(p.contract_type, "Desconocido"),
            p.num_pacientes_captados,
            f"{p.valor_por_paciente} USD ",
            f"{p.comision_total_calculada} USD",
        ]

        context.update({
            "title": f"Resumen del Perfil Administrativo",
            "table": {
                "headers": headers,
                "rows": [row],  # solo una fila
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())
    


@register_component
class ContactoAdministrativoComponent(BaseComponent):
    template_name = "admin/profile_card.html"
    name = "Información de Contacto"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        p = self.instance

        headers = ["Teléfono", "Correo electrónico", "Dirección", "Hoja de vida"]

        row = [
            p.phone_number.as_national if p.phone_number else "Sin número",
            p.email or "Sin correo",
            p.address or "Sin dirección",
            f'<a href="{p.resume.url}" target="_blank">Ver archivo</a>' if p.resume else "No disponible",
        ]

        context.update({
            "title": "Información de Contacto",
            "table": {
                "headers": headers,
                "rows": [row],
                "safe_html": True  # permite renderizar el <a> como HTML
            }
        })
        return context

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())

@admin.register(AdministrativeProfile)
class AdministrativeProfileAdmin(ModelAdmin):
    form = AdministrativeProfileForm
    list_display = ('full_name', 'get_job_title_display', 'get_department_display','salary', 'is_active')
    list_filter = ('job_title', 'department', 'is_active')
    list_sections = [PerfilAdministrativoComponent,ContactoAdministrativoComponent ]  # Agregar sección personalizada
    search_fields = ('first_name', 'last_name', 'email')
    list_editable = ('is_active',)
    list_per_page = 20

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    full_name.short_description = 'Nombre completo'

    def get_job_title_display(self, obj):
        return obj.get_job_title_display()
    get_job_title_display.short_description = 'Cargo'

    def get_department_display(self, obj):
        return obj.get_department_display()
    get_department_display.short_description = 'Departamento'





