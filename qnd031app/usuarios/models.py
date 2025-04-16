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



class prospecion_administrativa(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    especialidad = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especialidad")

    class Meta:
        ordering = ['user']
        verbose_name_plural = "Registros Administrativos / Ingreso de Prospecto de Paciente"
        verbose_name = "Administrativo / prospeciónes"

    def __str__(self):
        return 'Registro de prospecto : {}'.format(self.user.username)

class Perfil_Terapeuta(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    especialidad = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especialidad")

    class Meta:
        ordering = ['user']
        verbose_name = "Registro Administrativo / Ingreso de Terapista"
        verbose_name_plural = "Registro Administrativo / Ingreso de Terapista"

    def __str__(self):
        return 'Registro de Terapista: {}'.format(self.user.username)



class Profile(models.Model):
    #Informacion personal
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
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
    pago = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Saldo a cancelar")
    fecha_pago = models.DateField(blank=True, null=True, verbose_name="Fecha de pago")
    fecha_vencimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de vencimiento de pago")
    estado_de_pago = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            ('Pagado', 'Pagado'),
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
        ('Terapéutico', 'Terapéutico'),
        ('Solicitud de pago vencido', 'Solicitud de pago vencido'),
        ('Solicitud de Certificado Médico', 'Solicitud de Certificado Médico'),
        ('Reclamo del servicio  Médico', 'Reclamo del servicio  Médico'),
        ('Cancelación del servicio Médico', 'Cancelación del servicio Médico'),
    ]
    
    emisor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mensajes_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    asunto = models.CharField(max_length=50, choices=ASUNTOS_CHOICES, default='Consulta')  
    cuerpo = models.TextField(blank=True, null=True)
    leido = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_envio']
        verbose_name_plural = "Bandeja de entrada MEDDES"
        verbose_name = "Mensajes MEDDES"

    def __str__(self):
        fecha = self.fecha_envio.strftime("%d/%m/%Y %H:%M") if self.fecha_envio else "Sin fecha"
        return f"{self.emisor} - {fecha}"

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
    notas = models.TextField(blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=True)

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