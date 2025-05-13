from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.ec.forms import ECProvinceSelect
from ckeditor.fields import RichTextField
from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from datetime import date
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django_celery_results.models import TaskResult
from djmoney.models.fields import MoneyField
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from datetime import timedelta
from schedule.models import Event, Calendar
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware
from django.utils import timezone



class Prospeccion(models.Model):
    distrito = models.CharField("DISTRITO", max_length=100)
    provincia = models.CharField("PROVINCIA", max_length=100)
    zona = models.CharField("ZONA", max_length=100)
    nombre_institucion = models.CharField("NOMBRE DE LA INSTITUCIÓN", max_length=200)
    sostenimiento = models.CharField("SOSTENIMIENTO", max_length=100)
    estado = models.CharField("ESTADO", max_length=100)
    telefono = models.CharField("TELEFONO", max_length=100)
    sector = models.CharField("SECTOR", max_length=100)
    direccion = models.CharField("DIRECCION", max_length=250)

    tl_nombre_contacto = models.CharField("TERAPIA DE LENGUAJE \nNOMBRE DE CONTACTO", max_length=200)
    tl_cargo_contacto = models.CharField("TERAPIA DE LENGUAJE \nCARGO CONTACTO", max_length=200)
    tl_email = models.EmailField("TERAPIA DE LENGUAJE \nEMAIL", blank=True, null=True)
    tl_proceso_realizado = models.TextField("TERAPIA DE LENGUAJE\nPROCESO REALIZADO", blank=True)
    tl_responsable = models.CharField("TERAPIA DE LENGUAJE\nRESPONSABLE", max_length=200, blank=True)
    tl_fecha_contacto = models.DateField("TERAPIA DE LENGUAJE\nFECHA DE CONTACTO", blank=True, null=True)
    tl_observaciones = models.TextField("TL\nGENERAL OBSERVACIONES", blank=True)
    tl_fecha_proximo_contacto = models.DateField("TL\nFECHA PROXIMO CONTACTO", blank=True, null=True)

    psicologia_email = models.EmailField("PSICOLOGIA\nEMAIL", blank=True, null=True)
    psicologia_observaciones = models.TextField("P\nGENERAL OBSERVACIONES", blank=True)
    psicologia_fecha_proximo_contacto = models.DateField("P\nFECHA PROXIMO CONTACTO", blank=True, null=True)

    vya_observacion = models.TextField("VYA\nOBSERVACIÓN", blank=True)
    vya_observaciones = models.TextField("VYA\nGENERAL OBSERVACIONES", blank=True)
    vya_fecha_proximo_contacto = models.DateField("VYA\nFECHA PROXIMO\n CONTACTO", blank=True, null=True)

    class Meta:
        ordering = ['tl_fecha_contacto']
        verbose_name_plural = "Registros Administrativos / Prospección "
        verbose_name = "Administrativo / Prospecciones"

    def __str__(self):
        return self.nombre_institucion



class prospecion_administrativa(models.Model):
    ESTADOS = [
        ('por_contactar', 'Por Contactar'),
        ('contactado', 'Contactado'),
        ('en_cita', 'En Cita'),
        ('convenio_firmado', 'Convenio Firmado'),
        ('capacitacion', 'Capacitación'),
        ('valoracion', 'Valoración'),
        ('en_terapia', 'En Terapia'),
        ('rechazado', 'Rechazado'),
        ('finalizado', 'Finalizado'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=255, verbose_name="Nombre del Colegio",null=True, blank=True)
    estado = models.CharField(max_length=30, choices=ESTADOS, default='por_contactar',null=True, blank=True)    
    fecha_estado_actualizado = models.DateField(auto_now=True)
    sucursal = models.CharField(max_length=255,blank=True,null=True,
        choices=[
            ('Quito - Valles', 'Quito - Valles'),
            ('Quito - Centro', 'Quito - Centro'),
            ('Guayaquil', 'Guayaquil'),
            ('Manta', 'Manta'),
        ],
        verbose_name="Sucursal"
    )

    regional = models.CharField(max_length=100,null=True, blank=True)   
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True) 

    mails_colegio =models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico de Colegio")
    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )
    telefonos_colegio = PhoneNumberField(verbose_name="Teléfono de persona a cargo",validators=[phone_regex],default='+593')

    nombre_persona_cargo = models.CharField(max_length=150,null=True, blank=True)
    telefono_persona_cargo = models.CharField(max_length=50,null=True, blank=True)
    correo_persona_cargo = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico Persona a cargo")

    terapeutas_asignados = models.ManyToManyField('auth.User', limit_choices_to={'groups__name': 'Terapeutas'})
    ejecutivo_encargado = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='colegios_asignados')

    convenio_pdf = models.FileField(
        upload_to='convenios/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['pdf'])],
        help_text="Cargar archivo en PDF"
    )

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = "Registros Administrativos / Ingreso perfil de colegio"
        verbose_name = "Administrativo / Colegios"

    def alerta_estado_inactivo(self):
        if self.estado != 'inactivo':
            return False
        return timezone.now().date() - self.fecha_estado_actualizado > timedelta(days=15)
    
    alerta_estado_inactivo.boolean = True
    alerta_estado_inactivo.short_description = "Alerta de inactividad (15 días)"

    def __str__(self):
        return '{}'.format(self.colegio)





class Perfil_Terapeuta(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    especialidad = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especialidad")
    SEXO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    #usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_terapeuta')
    nombres_completos = models.CharField(max_length=200,null=True, blank=True)
    sucursal = models.CharField(max_length=255,blank=True,null=True,
        choices=[
            ('Quito - Valles', 'Quito - Valles'),
            ('Quito - Centro', 'Quito - Centro'),
            ('Guayaquil', 'Guayaquil'),
            ('Manta', 'Manta'),
        ],
        verbose_name="Sucursal"
    )
    edad = models.PositiveIntegerField(null=True, blank=True)   
    sexo = models.CharField(max_length=1, choices=SEXO_OPCIONES, null=True, blank=True) 
    fecha_nacimiento = models.DateField(null=True, blank=True)  
    cedula = models.CharField(max_length=20,null=True, blank=True)  
    fecha_ingreso = models.DateField(null=True, blank=True) 

    titulo_universitario = models.FileField(upload_to='documentos/terapeutas/titulo/', blank=True, null=True)
    antecedentes_penales = models.FileField(upload_to='documentos/terapeutas/antecedentes/', blank=True, null=True)
    certificados = models.FileField(upload_to='documentos/terapeutas/certificados/', blank=True, null=True)

    telefono = models.CharField(max_length=50, null =True, blank=True)  
    datos_bancarios = models.TextField(help_text="Ej: Banco, número de cuenta, tipo", null=True, blank=True)    
    pago_por_hora = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  
    tipo_servicio = models.CharField(max_length=100, null=True, blank=True)
    servicio_domicilio = models.BooleanField(default=False, null=True, blank=True)
    servicio_institucion = models.BooleanField(default=True, null=True, blank=True)


    class Meta:
        ordering = ['user']
        verbose_name = "Registro Administrativo / Ingreso de Terapista"
        verbose_name_plural = "Registro Administrativo / Ingreso de Terapista"

    def __str__(self):
        return 'Terapista: {}'.format(self.user.username)


class AsistenciaTerapeuta(models.Model):
    terapeuta = models.ForeignKey(Perfil_Terapeuta, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    evento = models.OneToOneField(Event, null=True, blank=True, on_delete=models.SET_NULL)
    #cita_relacionada = models.ForeignKey('Cita', on_delete=models.SET_NULL, null=True, blank=True)
    sucursal = models.CharField(max_length=255,blank=True,null=True,
        choices=[
            ('Quito - Valles', 'Quito - Valles'),
            ('Quito - Centro', 'Quito - Centro'),
            ('Guayaquil', 'Guayaquil'),
            ('Manta', 'Manta')
        ],
        verbose_name="Sucursal"
    )

    class Meta:
        unique_together = ('terapeuta', 'fecha', 'hora_entrada')
        ordering = ['-fecha', 'hora_entrada']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.evento:
            calendario, _ = Calendar.objects.get_or_create(name='terapeutas', slug='terapeutas')
            
            start = make_aware(datetime.combine(self.fecha, self.hora_entrada))
            end = make_aware(datetime.combine(self.fecha, self.hora_salida or self.hora_entrada))

            evento = Event.objects.create(
                title=f"Asistencia de {self.terapeuta.nombres_completos}",
                start=start,
                end=end,
                calendar=calendario,
                description=self.observaciones
            )
            self.evento = evento
            super().save(update_fields=['evento'])

    def __str__(self):
        return f"Asistencia {self.terapeuta.nombres_completos} - {self.fecha}"



class Profile(models.Model):
    #Informacion personal
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    sucursal = models.CharField(max_length=255,blank=True,null=True,
        choices=[
            ('Quito - Valles', 'Quito - Valles'),
            ('Quito - Centro', 'Quito - Centro'),
            ('Guayaquil', 'Guayaquil'),
            ('Manta', 'Manta')
        ],
        verbose_name="Sucursal"
    )
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, verbose_name="Foto Perfil")
    ruc = models.CharField(max_length=13, verbose_name="C.I Paciente", help_text="Ingrese C.I del Paciente",blank=True, null=True)
    nombre_paciente = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombres")
    apellidos_paciente = models.CharField(max_length=255, blank=True, null=True, verbose_name="Apellidos")
    nacionalidad = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nacionalidad")
    sexo = models.CharField(blank=True, null=True, max_length=120, choices=[("MASCULINO", "Masculino"), ("FEMENINO", "Femenino")], verbose_name="Sexo del Paciente")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")
    edad =  models.CharField(max_length=255, blank=True, null=True, verbose_name="Edad")
    unidad_educativa =  models.CharField(max_length=255, blank=True, null=True, verbose_name="Unidad educativa")
    #Informacion de representante y contacto
    nombres_representante_legal = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombres")
    apellidos_representante_legal = models.CharField(max_length=255, blank=True, null=True, verbose_name="Apellidos")
    relacion_del_representante = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            ('Padre', 'Padre'),
            ('Madre', 'Madre'),
            ('Hermano/a', 'Hermano/a'),
            ('Tío/a', 'Tío/a'),
            ('Abuelo/a', 'Abuelo/a'),
            ('Ñeto/a', 'Ñeto/a'),
            ('Tutor/a', 'Tutor/a'),
            ('Otro', 'Otro'),
        ],
        verbose_name="Relación del representante con el paciente"
    )
    nacionalidad_representante = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nacionalidad")
    ruc_representante = models.CharField(max_length=13, verbose_name="RUC / C.I", help_text="R.U.C o C.I del Representante",blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico")
    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )
    telefono = PhoneNumberField(verbose_name="Teléfono convencional de contacto",validators=[phone_regex],default='+593')
    celular = PhoneNumberField(verbose_name="Teléfono celular de contacto",validators=[phone_regex],default='+593')
    provincia = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            ('Azuay', 'Azuay'),
            ('Bolívar', 'Bolívar'),
            ('Cañar', 'Cañar'),
            ('Carchi', 'Carchi'),
            ('Chimborazo', 'Chimborazo'),
            ('Cotopaxi', 'Cotopaxi'),
            ('El Oro', 'El Oro'),
            ('Esmeraldas', 'Esmeraldas'),
            ('Galápagos', 'Galápagos'),
            ('Guayas', 'Guayas'),
            ('Imbabura', 'Imbabura'),
            ('Loja', 'Loja'),
            ('Los Ríos', 'Los Ríos'),
            ('Manabí', 'Manabí'),
            ('Morona Santiago', 'Morona Santiago'),
            ('Napo', 'Napo'),
            ('Orellana', 'Orellana'),
            ('Pastaza', 'Pastaza'),
            ('Pichincha', 'Pichincha'),
            ('Santa Elena', 'Santa Elena'),
            ('Santo Domingo de los Tsáchilas', 'Santo Domingo de los Tsáchilas'),
            ('Sucumbíos', 'Sucumbíos'),
            ('Tungurahua', 'Tungurahua'),
            ('Zamora Chinchipe', 'Zamora Chinchipe'),
        ],
        verbose_name="Localidad",
        default='Pichincha'
    )
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")
    actividad_economica =  models.CharField(max_length=255, blank=True, null=True, verbose_name="Actividad económica del representante")
    
    #Informacion de Terapeutica
    user_terapeuta = models.OneToOneField(Perfil_Terapeuta, on_delete=models.CASCADE, verbose_name="Terapéuta Asignado")
    valorizacion_terapeutica = models.TextField(blank=True, null=True, verbose_name="Valoración Terapéutica")
    tipo_servicio = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            ('Terapia de Lenguaje - valoración lenguaje', 'Terapia de Lenguaje - valoración lenguaje'),
            ('Terapia de Lenguaje - Terapia de lenguaje', 'Terapia de Lenguaje - Terapia de lenguaje'),
            ('Terapia de Lenguaje - paquete mensual(8 sesiones)', 'Terapia de Lenguaje - paquete mensual(8 sesiones)'),
            ('Terapia de Lenguaje - paquete mensual(24 sesiones)', 'Terapia de Lenguaje - paquete mensual(24 sesiones)'),
            ('Psicología - valoración Psicologica', 'Psicología - valoración Psicologica'),
            ('Psicología - valoración Psicopedagogica', 'Psicología - valoración Psicopedagogica'),
            ('Psicología - Terapia Psicologica', 'Psicología - Terapia Psicologica'),
            ('Psicología - Terapia Psicologica de pareja', 'Psicología - Terapia Psicologica de pareja'),
            ('Psicología - Paquete mensual de terapia (4 sesiones)', 'Psicología - Paquete mensual de terapia (4 sesiones)'),
            ('Psicología - Paquete mensual de terapia (12 sesiones)', 'Psicología - Paquete mensual de terapia (12 sesiones)'),
            ('Psicología - Paquete mensual de terapia de pareja', 'Psicología - Paquete mensual de terapia de pareja'),
            ('Psicología - Paquete mensual de terapia de pareja (12 sesiones)', 'Psicología - Paquete mensual de terapia de pareja (12 sesiones)'),
            ('Estimulación Cognitiva Adulto Mayor - Individual', 'Estimulación Cognitiva Adulto Mayor - Individual'),
            ('Estimulación Cognitiva Adulto Mayor - grupal (3-5)', 'Estimulación Cognitiva Adulto Mayor - grupal (3-5)'),
            ('Estimulación Cognitiva Adulto Mayor - Individual (8 sesiones)', 'Estimulación Cognitiva Adulto Mayor - Individual (8 sesiones)'),
            ('Audiologia Ocupacional', 'Audiologia Ocupacional'),
            ('Audiologia escolar', 'Audiologia escolar'),
            ('Audiologia - Limpieza de Oido', 'Audiologia - Limpieza de Oido'),
            ('Audiologia- lavado de oido', 'Audiologia- lavado de oido'),
        ],
        verbose_name="Servicio terapéutico"
    )
    fecha_inicio = models.DateField(blank=True, null=True, verbose_name="Fecha de inicio de tratamiento")
    fecha_terminacion = models.DateField(blank=True, null=True, verbose_name="Fecha de terminación de tratamiento")
    #Informacion de la cuenta


    class Meta:
        ordering = ['user']
        verbose_name = "Registro Administrativo / Ingreso de Paciente"
        verbose_name_plural = "Registro Administrativo / Ingreso de Paciente"   

    @property
    def edad_paciente(self):
        if self.fecha_nacimiento:
            today = date.today()
            nacimiento = self.fecha_nacimiento
            edad = today.year - nacimiento.year - ((today.month, today.day) < (nacimiento.month, nacimiento.day))
            return edad
        return None

    def save(self, *args, **kwargs):
        edad_calculada = self.edad_paciente
        if edad_calculada is not None:
            self.edad = str(edad_calculada)  # Lo guardamos como string ya que el campo es CharField
        else:
            self.edad = None
        super().save(*args, **kwargs)

    @property
    def nombre_completo(self):
        return f"{self.nombre_paciente} {self.apellidos_paciente}".strip()

    def __str__(self):
        return self.nombre_completo


class pagos(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    sucursal = models.CharField(max_length=255,blank=True,null=True,
        choices=[
            ('Quito - Valles', 'Quito - Valles'),
            ('Quito - Centro', 'Quito - Centro'),
            ('Guayaquil', 'Guayaquil'),
            ('Manta', 'Manta'),
        ],
        verbose_name="Sucursal"
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=True)
    cuenta = models.CharField(max_length=255, blank=True, null=True, verbose_name="Número de cuenta")
    colegio = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre del colegio")
    plan = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            ('Institucional', 'Institucional'),
            ('Domicilio Institucional', 'Domicilio Institucional'),
            ('Domicilio Familiar', 'Domicilio Familiar'),
            ('Consultorio Institucional', 'Consultorio Institucional'),
            ('Becas(100%)', 'Becas(100%)'),
            ('Becas(50%)', 'Becas(50%)'),
            ('Domicilio', 'Domicilio'),
            ('Consultorio', 'Consultorio'),
        ],
        verbose_name="Plan Económico"
    )
    convenio = models.BooleanField(default=False, verbose_name="Convenio")
    sucursal = models.CharField(max_length=255,blank=True,null=True,
        choices=[
            ('Quito - Valles', 'Quito - Valles'),
            ('Quito - Centro', 'Quito - Centro'),
            ('Guayaquil', 'Guayaquil'),
            ('Manta', 'Manta'),
        ],
        verbose_name="Sucursal"
    )
    servicio = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            ('Terapia de Lenguaje - valoración lenguaje', 'Terapia de Lenguaje - valoración lenguaje'),
            ('Terapia de Lenguaje - Terapia de lenguaje', 'Terapia de Lenguaje - Terapia de lenguaje'),
            ('Terapia de Lenguaje - paquete mensual(8 sesiones)', 'Terapia de Lenguaje - paquete mensual(8 sesiones)'),
            ('Terapia de Lenguaje - paquete mensual(24 sesiones)', 'Terapia de Lenguaje - paquete mensual(24 sesiones)'),
            ('Psicología - valoración Psicologica', 'Psicología - valoración Psicologica'),
            ('Psicología - valoración Psicopedagogica', 'Psicología - valoración Psicopedagogica'),
            ('Psicología - Terapia Psicologica', 'Psicología - Terapia Psicologica'),
            ('Psicología - Terapia Psicologica de pareja', 'Psicología - Terapia Psicologica de pareja'),
            ('Psicología - Paquete mensual de terapia (4 sesiones)', 'Psicología - Paquete mensual de terapia (4 sesiones)'),
            ('Psicología - Paquete mensual de terapia (12 sesiones)', 'Psicología - Paquete mensual de terapia (12 sesiones)'),
            ('Psicología - Paquete mensual de terapia de pareja', 'Psicología - Paquete mensual de terapia de pareja'),
            ('Psicología - Paquete mensual de terapia de pareja (12 sesiones)', 'Psicología - Paquete mensual de terapia de pareja (12 sesiones)'),
            ('Estimulación Cognitiva Adulto Mayor - Individual', 'Estimulación Cognitiva Adulto Mayor - Individual'),
            ('Estimulación Cognitiva Adulto Mayor - grupal (3-5)', 'Estimulación Cognitiva Adulto Mayor - grupal (3-5)'),
            ('Estimulación Cognitiva Adulto Mayor - Individual (8 sesiones)', 'Estimulación Cognitiva Adulto Mayor - Individual (8 sesiones)'),
            ('Audiologia Ocupacional', 'Audiologia Ocupacional'),
            ('Audiologia escolar', 'Audiologia escolar'),
            ('Audiologia - Limpieza de Oido', 'Audiologia - Limpieza de Oido'),
            ('Audiologia- lavado de oido', 'Audiologia- lavado de oido'),
        ],
        verbose_name="Servicio terapéutico"
    )

    fecha_emision_factura = models.DateField(blank=True, null=True, verbose_name="Fecha de emisión de factura")
    numero_factura = models.CharField(max_length=255, blank=True, null=True, verbose_name="Número de Factura")
    pago = MoneyField(
    max_digits=10,
    decimal_places=2,
    default_currency='USD',  # o 'PEN', 'ARS', etc.
    blank=True,
    null=True,
    verbose_name="Saldo a cancelar"
    )
    fecha_pago = models.DateField(blank=True, null=True, verbose_name="Fecha de pago")
    fecha_vencimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de vencimiento de pago")
    estado_de_pago = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            
            ('Al día', 'Al día'),
            ('Pendiente', 'Pendiente'),
            ('Vencido', 'Vencido'),
        ],
        verbose_name="Estado de pago"
    )
    comprobante_pago = models.FileField(upload_to='comprobantes/%Y/%m/%d/', blank=True, verbose_name="Comprobante de pago")
    numero_de_comprobante = models.CharField(max_length=255, blank=True, null=True, verbose_name="Número de comprobante de pago")
    banco = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            ('Banco Pichincha', 'Banco Pichincha'),
            ('Banco del Pacífico', 'Banco del Pacífico'),
            ('Produbanco', 'Produbanco'),
            ('Banco Internacional', 'Banco Internacional'),
            ('Banco Bolivariano', 'Banco Bolivariano'),
            ('Banco de Guayaquil', 'Banco de Guayaquil'),
            ('Banco del Austro', 'Banco del Austro'),
            ('Banco Solidario', 'Banco Solidario'),
            ('Cooperativa JEP', 'Cooperativa JEP'),
            ('Cooperativa 29 de Octubre', 'Cooperativa 29 de Octubre'),
            ('Cooperativa Policía Nacional', 'Cooperativa Policía Nacional'),
            ('Banco Central del Ecuador', 'Banco Central del Ecuador'),
            ('Banco Amazonas', 'Banco Amazonas'),
            ('Banco ProCredit', 'Banco ProCredit'),
            ('Banco Diners Club', 'Banco Diners Club'),
            ('Banco General Rumiñahui', 'Banco General Rumiñahui'),
            ('Banco Coopnacional', 'Banco Coopnacional'),
            ('Otros', 'Otros'),
            ('No aplica', 'No aplica'),
        ],
        verbose_name="Institución bancaria de Pago"
    )
    metodo_pago = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            ('Efectivo', 'Efectivo'),
            ('Transferencia Bancaria', 'Transferencia Bancaria'),
            ('Electónica - PayPhone', 'Electónica - PayPhone'),
            ('Electónica - DataFast', 'Electónica - DataFast'),
        ],
        verbose_name="Método de Pago"
    )

    class Meta:
        ordering = ['fecha_emision_factura']
        verbose_name_plural = "Registros Administrativos /Ingreso de Pagos por servicios Terapéuticos"
        verbose_name = "Administrativo / Pagos servicios "

    def __str__(self):
        return "Pagos de servicio Paciente: {}".format(self.user.username)

    def save(self, *args, **kwargs):
        # Verificamos que ambas fechas estén presentes
        if self.fecha_emision_factura and self.fecha_vencimiento:
            diferencia = (self.fecha_vencimiento - self.fecha_emision_factura).days
            if diferencia < 30:
                self.estado_de_pago = 'Pendiente'
            else:
                self.estado_de_pago = 'Vencido'
        super().save(*args, **kwargs)

class tareas(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    terapeuta = models.OneToOneField(Perfil_Terapeuta, on_delete=models.CASCADE, verbose_name="Terapéuta Asignado")
    titulo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Título de la tarea") 
    fecha_envio = models.DateField(blank=True, null=True, verbose_name="Fecha de envio de tarea")
    fecha_entrega = models.DateField(blank=True, null=True, verbose_name="Fecha de entrega de tarea")
    material_adjunto =  models.FileField(upload_to='materiales/%Y/%m/%d/', blank=True, verbose_name="Material adjunto")
    media_terapia =  models.FileField(upload_to='Videos/%Y/%m/%d/', blank=True, verbose_name="Contenido Multimedia de Terapia")
    descripcion_tarea = models.TextField(blank=True, null=True,verbose_name="Descripción de la tarea")
    sucursal = models.CharField(max_length=255,blank=True,null=True,
        choices=[
            ('Quito - Valles', 'Quito - Valles'),
            ('Quito - Centro', 'Quito - Centro'),
            ('Guayaquil', 'Guayaquil'),
            ('Manta', 'Manta'),
        ],
        verbose_name="Sucursal"
    )



    class Meta:
        ordering = ['user']
        verbose_name_plural = "Registros de Terapéuticos / Ingreso de Tareas Terapéuticas"
        verbose_name = "Paciente/ Tareas"

    def __str__(self):
        return "Tareas terapéuticas {}".format(self.user.username)

    


class Mensaje(models.Model):
    ASUNTOS_CHOICES = [
        ('Consulta', 'Consulta'),
        ('Sugerencia', 'Sugerencia'),   
        ('Informativo', 'Informativo'),
        ('Terapéutico', 'Terapeutico'),
        ('Solicitud de pago vencido', 'Solicitud de pago vencido'),
        ('Solicitud de Certificado Médico', 'Solicitud de Certificado Medico'),
        ('Reclamo del servicio  Médico', 'Reclamo del servicio  Médico'),
        ('Cancelación del servicio Médico', 'Cancelación del servicio Médico'),
    ]
    
    emisor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mensajes_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    asunto = models.CharField(max_length=50, choices=ASUNTOS_CHOICES, default='Consulta')  
    cuerpo = RichTextField(blank=True, null=True)
    leido = models.BooleanField(default=False)
    creado = models.DateTimeField(default=timezone.now)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    sucursal = models.CharField(max_length=255,blank=True,null=True,
        choices=[
            ('Quito - Valles', 'Quito - Valles'),
            ('Quito - Centro', 'Quito - Centro'),
            ('Guayaquil', 'Guayaquil'),
            ('Manta', 'Manta'),
        ],
        verbose_name="Sucursal"
    )

    # ➕ Campo para vincular con Celery
    task_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID de la tarea de Celery asociada")
    task_status = models.CharField(max_length=50, blank=True, null=True, help_text="Estado de la tarea de Celery asociada")

    class Meta:
        ordering = ['-fecha_envio']
        verbose_name_plural = "Bandeja de entrada MEDDES"
        verbose_name = "Mensajes MEDDES"

    def __str__(self):
        fecha = self.fecha_envio.strftime("%d/%m/%Y %H:%M") if self.fecha_envio else "Sin fecha"
        return f"{self.emisor} - {fecha}"

    @property
    def estado_tarea(self):
        """Devuelve el estado de la tarea de Celery asociada, si existe"""
        if self.task_id:
            task_result = TaskResult.objects.filter(task_id=self.task_id).order_by('-date_done').first()
            if task_result:
                return task_result.task_state  # o .status si prefieres
            return "Desconocido"
        return "No asignada"

    def save(self, *args, **kwargs):
        """Sobrescribe el método save para actualizar el estado de la tarea"""
        if self.task_id:
            task_result = TaskResult.objects.filter(task_id=self.task_id).order_by('-date_done').first()
            if task_result:
                self.task_status = task_result.task_state  # Actualiza el estado de la tarea
            else:
                self.task_status = "Desconocido"
        else:
            self.task_status = "No asignada"
        super().save(*args, **kwargs)


class Cita(models.Model):
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='citas_creadas',
        on_delete=models.CASCADE
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='citas_recibidas',
        on_delete=models.CASCADE
    )
    fecha = models.DateTimeField()
    fecha_final = models.DateTimeField(null=True, blank=True)
    motivo = models.CharField(max_length=255)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada'),
        ],
        default='pendiente'
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    notas = models.TextField(blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=True)
    sucursal = models.CharField(max_length=255,blank=True,null=True,
        choices=[
            ('Quito - Valles', 'Quito - Valles'),
            ('Quito - Centro', 'Quito - Centro'),
            ('Guayaquil', 'Guayaquil'),
            ('Manta', 'Manta'),
        ],
        verbose_name="Sucursal"
    )
    

    class Meta:
        
        ordering = ['-fecha']
        verbose_name_plural = "Registros Administrativos / Ingreso de Citas"
        verbose_name = "Administrativos / Ingreso de Cita"

def __str__(self):
    return f"{self.creador} → {self.destinatario} ({self.fecha.strftime('%d/%m/%Y %H:%M')})"

class Dashboard(models.Model):
    titulo = models.CharField(max_length=100)
    informacion_basica = RichTextField()
    bloque_1 = RichTextField(blank=True, null=True)
    bloque_2 = RichTextField(blank=True, null=True)
    bloque_3 = RichTextField(blank=True, null=True)
    bloque_4 = RichTextField(blank=True, null=True)
    bloque_5 = RichTextField(blank=True, null=True)
    link_soporte_tecnico = models.URLField()

    def __str__(self):
        return self.titulo
    title = models.CharField(max_length=100)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BitacoraDesarrollo(models.Model):
    TIPO_SISTEMA_CHOICES = [
        ('RAPP', 'Registro administrativo/Perfil de Paciente'),
        ('RAPT', 'Registro administrativo/Perfil de Terapistas'),
        ('RAACC', 'Registro administrativo/Agenda de Citas Regulares'),
        ('RAPA', 'Registro administrativo/Prospeción Administrativa'),
        ('RAPS', 'Registro administrativo/Pago de Servicios'),
        ('RTTA', 'Registro Terapeutico/Tareas & Actividades'),
        ('RTAA', 'Registro Terapeutico/Asistencias'),
        ('SBN ', 'Bandeja de Notificaciones'),
        ('SERP', 'Visualización de ERP '),
    ]

    TIPO_TECHNOLOGIAS_CHOICES = [
        ('UX', 'Experiencia de Usuario'),
        ('UI', 'Interfase'),
        ('I+D', 'Implementación'),
        ('A', 'Automatización'),
    ]

    VERSION = [
        ('QND0301', 'QND-0.3.0.1'),
        ('QND0302', 'QND-0.3.0.2'),
        ('QND0303', 'QND-0.3.0.3'),
        ('QND0304', 'QND-0.3.0.4'),
    ]

    SQCREW = [
        ('DeV', 'Desarollo - backend'),
        ('DeV', 'Desarollo - frontend'),
        ('DeV', 'Desarollo - fullstack'),
        ('DeV', 'Desarollo - QA'),
        ('DeV', 'Desarollo - UI/UX'),
        ('DeV', 'Desarollo - I+D'),
        ('ProD', 'Producción -backend'),
        ('ProD', 'Producción - frontend'),
        ('ProD', 'Producción - fullstack'),
        ('ProD', 'Producción - QA'),
        ('ProD', 'Producción - UI/UX'),
        ('ProD', 'Producción - I+D'),
        ('StG', 'Soporte - backend'),
        ('StG', 'Soporte - frontend'),
        ('StG', 'Soporte - fullstack'),
        ('StG', 'Soporte - QA'),
        ('StG', 'Soporte - UI/UX'),
        ('StG', 'Soporte - I+D'),
        ('StG', 'Soporte - Producción'),
        ('DA', 'Data Analytics'),
    ]

    INCHARGE = [
        ('DeV', 'Mauricio Silva'),
        ('Prod', 'Andres Espinoza'),
        ('Front', 'Virginia Lasta'),
    ]

    STATE = [
        ('Revisión', 'Revisión'),
        ('Desarollo', 'Desarollo'),
        ('Pruebas', 'Pruebas'),
        ('Producción', 'Producción'),
        ('Aprobado', 'Aprobado'),
    ]

    version_relacionada = models.CharField(blank=True, null=True, max_length=200, choices=VERSION, verbose_name="Versión", default="QND-0.3.0.1")
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField(blank=True, null=True)  # nuevo campo automático
    incarge = models.CharField(blank=True, null=True,max_length=200, choices=INCHARGE)
    SmartQuail_Tech = models.CharField(max_length=200, choices=SQCREW,null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_cambio = models.CharField(max_length=200, choices=TIPO_SISTEMA_CHOICES)
    tipo_tecnologia = models.CharField(max_length=200, choices=TIPO_TECHNOLOGIAS_CHOICES)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    progreso = models.PositiveIntegerField(default=0) 
    estado =  models.CharField(blank=True, null=True, max_length=200, choices=STATE, verbose_name="ESTADO",default="Revisión")

    class Meta:
        verbose_name = "Entrada de Bitácora"
        verbose_name_plural = "Bitácora de Desarrollo QND.0.3.0.1"
        ordering = ['-fecha']

    def __str__(self):
        return f"[{self.fecha.strftime('%Y-%m-%d')}] {self.titulo} - {self.autor.username}"

    def save(self, *args, **kwargs):
        if not self.fecha_entrega:
            self.fecha_entrega = (timezone.now() + timedelta(days=5)).date()
        super().save(*args, **kwargs)
