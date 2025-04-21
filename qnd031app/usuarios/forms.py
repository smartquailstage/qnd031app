from django import forms
from django.contrib.auth.models import User, Group
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.forms import DateInput
from .models import Mensaje
from ckeditor.widgets import CKEditorWidget

class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario")
    password = forms.CharField(widget=forms.PasswordInput,label="Contraseña")

    

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        cuerpo = forms.CharField(widget=CKEditorWidget())
        fields = ['asunto', 'cuerpo']
        widgets = {
            'asunto': forms.Select(attrs={'class': 'form-select'}),
            #'receptor': forms.Select(attrs={'class': 'form-select'}),
            'cuerpo': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }

class LeidoForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['leido']
        widgets = {
            'leido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }