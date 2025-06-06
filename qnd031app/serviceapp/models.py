from django.db import models
from djmoney.models.fields import MoneyField
# Create your models here.



class ServicioTerapeutico(models.Model):
    LUGAR_CHOICES = [
        ('INSTITUCIONAL', 'Institucional'),
        ('DOMICILIO', 'Domicilio'),
        ('CONSULTA', 'Consulta'),
    ]


    TIPO_SERVICIO = [
        ('TERAPIA DE LENGUAJE', 'Terapia de Lenguaje'),
        ('ESTIMULACIÓN COGNITIVA', 'Estimulación Cognitiva'),
        ('PSICOLOGÍA', 'Psicología'),
        ('ESTIMULACIÓN TEMPRANA', 'Estimulación Temprana'),
        ('VALORACIÓN', 'Valoración'),
    ]

    lugar_servicio = models.CharField(
        max_length=50,
        choices=LUGAR_CHOICES,
        default='INSTITUCIONAL',
        verbose_name="Lugar donde se ofrece el servicio"
    )

    servicio = models.CharField(
        max_length=255,
        choices=TIPO_SERVICIO,
        unique=True,
        verbose_name="Servicio terapéutico"
    )

    costo_por_sesion = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',  # o 'PEN', 'ARS', etc.
        blank=True,
        null=True,
        verbose_name="Valor por sesión"
    ) 
    fecha_ingreso = models.DateField(null=True, blank=True)
    titulo_universitario = models.FileField(upload_to='documentos/terapeutas/titulo/', blank=True, null=True)
    antecedentes_penales = models.FileField(upload_to='documentos/terapeutas/antecedentes/', blank=True, null=True)
    certificados = models.FileField(upload_to='documentos/terapeutas/certificados/', blank=True, null=True)
    observacion = models.TextField(blank=True, null=True, verbose_name="Observación de servicio")

    activo = models.BooleanField(default=True, verbose_name="¿Servicio activo?")

    class Meta:
        verbose_name = "Servicio Terapéutico"
        verbose_name_plural = "Servicios Terapéuticos"
        ordering = ['servicio']

    def __str__(self):
        return f"{self.servicio} - {self.lugar_servicio} - {self.costo_por_sesion}"