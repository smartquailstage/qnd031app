from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class subscription_info(TranslatableModel):
        name=models.CharField(max_length=200, db_index=True)
        slug=models.SlugField(max_length=200, unique=True)
        inicio=models.DateTimeField(null=True)
        final=models.DateTimeField(null=True)
        desde=models.CharField(max_length=200, null=True)
        description=models.TextField(blank=True, null=True)
        contract=models.FileField(upload_to='tours/%Y/%m/%d', null=True)

class Meta:
    verbose_name = 'Billing info'
    verbose_name_plural = 'Billing info'

        def __str__(self):
            return self.safe_translation_getter('name', str(self.id))

