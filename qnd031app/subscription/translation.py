from .models import subscription_info, Contract          
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(subscription_info)
class subscription_info(TranslationOptions):
    fields = ('name','slug','inicio','final','desde','description','contract')


