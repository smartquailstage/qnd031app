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


class CustomTimePickerWidget(forms.TimeInput):
    template_name = 'admin/widgets/custom_timepicker.html'

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/clockpicker/0.0.7/bootstrap-clockpicker.min.css',
            )
        }
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/clockpicker/0.0.7/bootstrap-clockpicker.min.js',
        )



class CustomDateTimePickerWidget(forms.DateTimeInput):
    input_type = 'datetime-local'

    def __init__(self, attrs=None, format=None):
        format = format or '%Y-%m-%dT%H:%M'
        super().__init__(attrs=attrs, format=format)

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/datepicker/0.6.5/datepicker.min.css',
            )
        }
        js = (
            'https://code.jquery.com/jquery-3.4.1.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/datepicker/0.6.5/datepicker.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/datepicker/0.6.5/i18n/datepicker.es-ES.min.js',
        )