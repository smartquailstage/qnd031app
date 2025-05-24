# widgets.py
from django import forms

class CustomDatePickerWidget(forms.DateInput):
    template_name = 'admin/widgets/custom_datepicker.html'

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/datepicker/0.6.5/datepicker.min.css',),
        }
        js = (
            'https://code.jquery.com/jquery-3.4.1.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/datepicker/0.6.5/datepicker.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/datepicker/0.6.5/i18n/datepicker.es-ES.min.js',
        )