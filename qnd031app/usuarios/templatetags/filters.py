# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except Exception:
        return None

@register.filter
def dict_get(d, key):
    return d.get(key)
