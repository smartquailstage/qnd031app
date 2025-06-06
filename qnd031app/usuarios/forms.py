from django import forms
from django.contrib.auth.models import User, Group
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.forms import DateInput
from .models import Mensaje, Cita ,TareaComentario
from usuarios.models import ServicioTerapeutico
from ckeditor.widgets import CKEditorWidget
from django.forms.models import inlineformset_factory
from .models import prospecion_administrativa, DocenteCapacitado, Perfil_Terapeuta, ValoracionTerapia
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from .widgets import CustomDatePickerWidget


class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario")
    password = forms.CharField(widget=forms.PasswordInput,label="Contraseña")

    

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['cuerpo']
        widgets = {
            'cuerpo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Escribe tu mensaje aquí...'
            }),
        }

class LeidoForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['leido']
        widgets = {
            'leido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MarcarLeidoForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = []

class CitaForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Fecha y hora de la cita"
    )

    class Meta:
        model = Cita
        fields = ['motivo', 'fecha']

class TareaComentarioForm(forms.ModelForm):
    class Meta:
        model = TareaComentario
        fields = ['mensaje', 'archivo']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ServicioTerapeuticoForm(forms.ModelForm):
    TIPO_SERVICIO = [
        ('TERAPIA DE LENGUAJE', 'Terapia de Lenguaje'),
        ('ESTIMULACIÓN COGNITIVA', 'Estimulación Cognitiva'),
        ('PSICOLOGÍA', 'Psicología'),
        ('ESTIMULACIÓN TEMPRANA', 'Estimulación Temprana'),
        ('VALORACIÓN TERAPEUTICA', 'Valoración Terapeutica'),
    ]

    tipos = forms.MultipleChoiceField(
        choices=TIPO_SERVICIO,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tipo de servicio"
    )

    class Meta:
        model = ServicioTerapeutico
        fields = '__all__'

    def clean_tipos(self):
        return self.cleaned_data['tipos']


DocenteCapacitadoFormSet = inlineformset_factory(
    prospecion_administrativa,
    DocenteCapacitado,
    fields=[
        'fecha_capacitacion', 'area_capacitacion', 'tema',
        'nombres', 'apellidos', 'correo', 'cedula', 'telefono'
    ],
    extra=1,
    can_delete=True,
    max_num=100
)


class ProspecionAdministrativaForm(forms.ModelForm):
    class Meta:
        model = prospecion_administrativa
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.docentes_formset = DocenteCapacitadoFormSet(
            instance=self.instance,
            data=kwargs.get('data') if kwargs.get('data') else None
        )

    def is_valid(self):
        return super().is_valid() and self.docentes_formset.is_valid()

    def save(self, commit=True):
        instance = super().save(commit)
        self.docentes_formset.instance = instance
        self.docentes_formset.save()
        return instance



class PerfilTerapeutaForm(forms.ModelForm):
    class Meta:
        model = Perfil_Terapeuta
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': CustomDatePickerWidget(),
        }


class PerfilTerapeutaAdminForm(forms.ModelForm):
    TIPO_SERVICIO = Perfil_Terapeuta.TIPO_SERVICIO

    tipos = forms.MultipleChoiceField(
        choices=TIPO_SERVICIO,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tipo de servicio (múltiples opciones)",
        help_text="Selecciona uno o más tipos"
    )

    class Meta:
        model = Perfil_Terapeuta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convierte la lista JSON en lista normal
        if self.instance and self.instance.pk:
            self.initial['tipos'] = self.instance.tipos

    def clean_tipos(self):
        # Devuelve como lista para guardar en JSONField
        return self.cleaned_data['tipos']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipos = self.cleaned_data.get('tipos', [])
        if commit:
            instance.save()
            self.save_m2m()
        return instance

        
class PerfilPacientesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': CustomDatePickerWidget(),
        }

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = ValoracionTerapia
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': CustomDatePickerWidget(),
            'fecha_valoracion': CustomDatePickerWidget(),   
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class ProfileAdminForm(forms.ModelForm):
    TIPO_SERVICIO = [
        ('TERAPIA DE LENGUAJE', 'Terapia de Lenguaje'),
        ('ESTIMULACIÓN COGNITIVA', 'Estimulación Cognitiva'),
        ('PSICOLOGÍA', 'Psicología'),
        ('ESTIMULACIÓN TEMPRANA', 'Estimulación Temprana'),
        ('VALORACIÓN', 'Valoración'),
    ]

    tipos = forms.MultipleChoiceField(
        choices=TIPO_SERVICIO,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Servicios Terapéuticos",
        help_text="Seleccionar uno o más servicios"
    )

    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['tipos'] = self.instance.tipos or []

    def clean_tipos(self):
        return self.cleaned_data['tipos']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipos = self.cleaned_data.get('tipos', [])
        if commit:
            instance.save()
            self.save_m2m()
        return instance