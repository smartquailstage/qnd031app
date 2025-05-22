from django import forms
from django.contrib.auth.models import User, Group
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.forms import DateInput
from .models import Mensaje, Cita ,TareaComentario,ServicioTerapeutico 
from ckeditor.widgets import CKEditorWidget
from django.forms.models import inlineformset_factory
from .models import prospecion_administrativa, DocenteCapacitado


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