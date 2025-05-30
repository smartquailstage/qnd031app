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
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError



class Sucursal(models.Model):
    nombre = models.CharField("Nombre de la Sucursal", max_length=100)
    direccion = models.CharField("Dirección", max_length=255)
    telefonos = models.CharField("Teléfonos de Contacto", max_length=100, help_text="Separar múltiples teléfonos con comas.")
    persona_encargada = models.CharField("Persona Encargada", max_length=100)
    correo = models.EmailField("Mail de la Sucursal")

    def __str__(self):
        return self.nombre


class ServicioTerapeutico(models.Model):
    SERVICIOS = [
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
    ]

    TIPO_SERVICIO = [
        ('TERAPIA DE LENGUAJE', 'Terapia de Lenguaje'),
        ('ESTIMULACIÓN COGNITIVA', 'Estimulación Cognitiva'),
        ('PSICOLOGÍA', 'Psicología'),
        ('ESTIMULACIÓN TEMPRANA', 'Estimulación Temprana'),
    ]

    servicio = models.CharField(
        max_length=255,
        choices=SERVICIOS,
        unique=True,
        verbose_name="Servicio terapéutico"
    )

    costo_por_sesion = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Costo por sesión ($)"
    )

    tipos = models.JSONField(
        default=list,
        verbose_name="Tipo de servicio (múltiples opciones)",
        help_text="Selecciona uno o más tipos"
    )

    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del servicio")

    activo = models.BooleanField(default=True, verbose_name="¿Servicio activo?")

    class Meta:
        verbose_name = "Servicio Terapéutico"
        verbose_name_plural = "Servicios Terapéuticos"
        ordering = ['servicio']

    def __str__(self):
        return f"{self.servicio} - ${self.costo_por_sesion:.2f}"


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

    nombre = models.ForeignKey(
        'Prospeccion',
        on_delete=models.CASCADE,
        related_name="instituciones",
        null=True,
        blank=True
    )

    es_por_contactar = models.BooleanField(default=False, verbose_name="¿Se intentó contactar?")
    es_contactado = models.BooleanField(default=False, verbose_name="¿Ya fue contactado?")
    es_en_cita = models.BooleanField(default=False, verbose_name="¿Ya tuvo cita?")
    es_convenio_firmado = models.BooleanField(default=False, verbose_name="¿Firmó convenio?")
    es_capacitacion = models.BooleanField(default=False, verbose_name="¿Recibió capacitación?")
    es_valoracion = models.BooleanField(default=False, verbose_name="¿Tuvo valoración?")
    es_en_terapia = models.BooleanField(default=False, verbose_name="¿Recibe terapia?")
    es_rechazado = models.BooleanField(default=False, verbose_name="¿Fue rechazado?")
    es_finalizado = models.BooleanField(default=False, verbose_name="¿Finalizó el proceso?")
    es_inactivo = models.BooleanField(default=False, verbose_name="¿Está inactivo?")
    fecha_estado_actualizado = models.DateField(auto_now=True)

    sucursal = models.ForeignKey(
        'Sucursal',
        on_delete=models.CASCADE,
        related_name="sucursal9",
        null=True,
        blank=True
    )

    CIUDADES_ECUADOR = [(city, city) for city in [
        'Ambato', 'Arenillas', 'Atacames', 'Atuntaqui', 'Azogues', 'Babahoyo',
        'Bahía de Caráquez', 'Balzar', 'Baños de Agua Santa', 'Buena Fé', 'Calceta', 'Cañar',
        'Cariamanga', 'Catamayo', 'Cayambe', 'Chone', 'Cuenca', 'Daule', 'Durán', 'El Carmen',
        'El Guabo', 'El Triunfo', 'Esmeraldas', 'Gualaceo', 'Guaranda', 'Guayaquil',
        'Huaquillas', 'Ibarra', 'Jaramijó', 'Jipijapa', 'La Concordia', 'La Libertad',
        'La Maná', 'Latacunga', 'La Troncal', 'Loja', 'Lomas de Sargentillo', 'Macará',
        'Macas', 'Machachi', 'Machala', 'Manta', 'Milagro', 'Montalvo', 'Montecristi',
        'Naranjal', 'Naranjito', 'Nueva Loja', 'Otavalo', 'Pasaje', 'Pedernales', 'Pedro Carbo',
        'Piñas', 'Playas', 'Portoviejo', 'Puerto Baquerizo Moreno', 'Puerto Francisco de Orellana',
        'Puyo', 'Quevedo', 'Quito', 'Riobamba', 'Rosa Zárate', 'Salcedo', 'Salinas',
        'Samborondón', 'San Gabriel', 'Sangolquí', 'San Lorenzo', 'Santa Elena', 'Santa Rosa',
        'Santo Domingo de los Colorados', 'Shushufindi', 'Tena', 'Tulcán', 'Valencia',
        'Velasco Ibarra', 'Ventanas', 'Vinces', 'Yaguachi', 'Zamora'
    ]]

    ciudad = models.CharField(max_length=100, choices=CIUDADES_ECUADOR, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)

    mail_institucion_general = models.EmailField(blank=True, null=True, verbose_name="Mail General de la Institución")

    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )

    telefonos_colegio = PhoneNumberField(
        verbose_name="Teléfono de la Institución",
        validators=[phone_regex],
        default='+593'
    )

    # Responsable Institucional 1
    responsable_institucional_1 = models.CharField(max_length=150, null=True, blank=True, verbose_name="Responsable Institucional 1")
    cargo_responsable_1 = models.CharField(max_length=150, null=True, blank=True)
    telefono_responsable_1 = PhoneNumberField(verbose_name="Teléfono responsable 1", validators=[phone_regex], default='+593')
    mail_responsable_1 = models.EmailField(blank=True, null=True)

    # Responsable Institucional 2
    responsable_institucional_2 = models.CharField(max_length=150, null=True, blank=True, verbose_name="Responsable Institucional 2")
    cargo_responsable_2 = models.CharField(max_length=150, null=True, blank=True)
    telefono_responsable_2 = PhoneNumberField(verbose_name="Teléfono responsable 2", validators=[phone_regex], default='+593')
    mail_responsable_2 = models.EmailField(blank=True, null=True)

    # Terapeutas
    terapeutas_asignados = models.ManyToManyField(
        'Perfil_Terapeuta',
        related_name='instituciones_asignadas_terapeuta',
        verbose_name="Terapeutas Asignados"
    )

    # Ejecutivo Meddes
    ejecutivo_meddes = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='instituciones_asignadas',
        verbose_name="Ejecutivo Meddes"
    )
    cargo_ejecutivo_meddes = models.CharField(max_length=150, null=True, blank=True)
    telefono_ejecutivo_meddes = models.CharField(max_length=50, null=True, blank=True)
    mail_ejecutivo_meddes = models.EmailField(blank=True, null=True)

    convenio_pdf = models.FileField(
        upload_to='convenios/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['pdf'])],
        help_text="Cargar archivo en PDF"
    )

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = "Registros Administrativos / Ingreso perfil de institución"
        verbose_name = "Administrativo / Institución"

    def alerta_estado_inactivo(self):
        if self.estado != 'inactivo':
            return False
        return timezone.now().date() - self.fecha_estado_actualizado > timedelta(days=15)

    alerta_estado_inactivo.boolean = True
    alerta_estado_inactivo.short_description = "Alerta de inactividad (15 días)"

    def __str__(self):
        return str(self.nombre) if self.nombre else "Institución sin nombre"


class DocenteCapacitado(models.Model):
    AREA_CAPACITACION = [
        ('lenguaje', 'Lenguaje'),
        ('psicologia', 'Psicología'),
    ]

    institucion = models.ForeignKey(
        prospecion_administrativa,
        on_delete=models.CASCADE,
        related_name="docentes_capacitados"
    )
    fecha_capacitacion = models.DateField()
    area_capacitacion = models.CharField(max_length=50, choices=AREA_CAPACITACION)
    tema = models.CharField(max_length=255)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField()
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Docente Capacitado"
        verbose_name_plural = "Docentes Capacitados"

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.institucion.nombre}"









class Perfil_Terapeuta(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Elegir nombre de usuario en el sistema")
    especialidad = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especialidad")

    SEXO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    nombres_completos = models.CharField(max_length=200, null=True, blank=True)
    
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal10",null=True, blank=True
    )
    correo = models.EmailField(verbose_name="Correo Electrónico", null=True, blank=True)

    edad = models.PositiveIntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_OPCIONES, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)

    titulo_universitario = models.FileField(upload_to='documentos/terapeutas/titulo/', blank=True, null=True)
    antecedentes_penales = models.FileField(upload_to='documentos/terapeutas/antecedentes/', blank=True, null=True)
    certificados = models.FileField(upload_to='documentos/terapeutas/certificados/', blank=True, null=True)

    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )
    telefonos_contacto = PhoneNumberField(verbose_name="Teléfono de persona a cargo",validators=[phone_regex],default='+593')
    TIPO_CUENTA_CHOICES = [
        ('ahorros', 'Ahorros'),
        ('corriente', 'Corriente'),
    ]

    BANCOS_ECUADOR_CHOICES = [
        ('pichincha', 'Banco Pichincha'),
        ('guayaquil', 'Banco Guayaquil'),
        ('pacifico', 'Banco del Pacífico'),
        ('produbanco', 'Produbanco'),
        ('internacional', 'Banco Internacional'),
        ('austro', 'Banco del Austro'),
        ('machala', 'Banco de Machala'),
        ('bolivariano', 'Banco Bolivariano'),
        ('promerica', 'Banco Promerica'),
        ('coopjep', 'Cooperativa JEP'),
        ('cooperco', 'Cooperco'),
        ('mutualista_pichincha', 'Mutualista Pichincha'),
        ('', 'Otro'),  # Opción para otros bancos
        # Agrega más si es necesario
    ]

    banco = models.CharField(
        "Banco", max_length=50, choices=BANCOS_ECUADOR_CHOICES,
        blank=True, null=True, help_text="Selecciona el banco"
    )
    tipo_cuenta = models.CharField(
        "Tipo de cuenta", max_length=20, choices=TIPO_CUENTA_CHOICES,
        blank=True, null=True
    )
    numero_cuenta = models.CharField("Número de cuenta", max_length=30, blank=True, null=True)
   # cedula_titular = models.CharField("Cédula del Terapeuta", max_length=20, blank=True, null=True)
    #nombre_titular = models.CharField("Nombre del titular", max_length=100, blank=True, null=True)
    pago_por_hora = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    tipo_servicio = models.ManyToManyField('ServicioTerapeutico',
    related_name='servicios_terapeuticos1',
    verbose_name="Servicio terapéutico",
    blank=True
    )
    servicio_domicilio = models.BooleanField(default=False, null=True, blank=True)
    servicio_institucion = models.BooleanField(default=True, null=True, blank=True)
    activo = models.BooleanField(default=True, verbose_name="¿Terapeuta activo?")
    class Meta:
        ordering = ['user']
        verbose_name = "Registro Administrativo / Ingreso de Terapista"
        verbose_name_plural = "Registro Administrativo / Ingreso de Terapista"

    def __str__(self):
        return f'{self.user.get_full_name()}'



class ValoracionTerapia(models.Model):
    perfil_terapeuta =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='perfil_terapeuta_asignado',
        on_delete=models.CASCADE,
        verbose_name="Terapeuta Responsable",
        null=True,
        blank=True
    )

    # Reemplazamos el campo tipo_valoracion por booleanos
    es_particular = models.BooleanField(default=False, verbose_name="Valoración Particular")
    es_convenio = models.BooleanField(default=False, verbose_name="Valoración por Convenio")

    fecha_valoracion = models.DateField(verbose_name="Fecha de Valoración")
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Paciente Valorado")
    fecha_nacimiento = models.DateField()

    @property
    def edad(self):
        today = date.today()
        if self.fecha_nacimiento:
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None

    institucion = models.ForeignKey(
        prospecion_administrativa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Institución"
    )

    grado = models.CharField(max_length=100, blank=True, null=True)
    servicio = models.ForeignKey(
        'ServicioTerapeutico',
        on_delete=models.CASCADE,
        related_name='servicios_terapeuticos2',
        verbose_name="Servicio terapéutico", null=True, blank=True
    )

    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal1", null=True, blank=True
    )

    proceso_terapia = models.BooleanField(default=False, verbose_name="Proceso de Terapia")
    diagnostico = models.TextField(blank=True, null=True)

    fecha_asesoria = models.DateField(null=True, blank=True)
    recibe_asesoria = models.BooleanField(default=False)

    observaciones = models.TextField(blank=True, null=True)

    archivo_adjunto = models.FileField(
        upload_to='valoraciones/adjuntos/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Valoración Terapéutica"
        verbose_name_plural = "Valoraciones Terapéuticas"
        ordering = ['-fecha_valoracion']

    def save(self, *args, **kwargs):
        if self.es_particular and self.es_convenio:
            raise ValueError("Solo una opción puede estar activa: 'particular' o 'convenio'")
        super().save(*args, **kwargs)

    def __str__(self):
        tipo = "Particular" if self.es_particular else "Convenio" if self.es_convenio else "Sin especificar"
        return f"{self.nombre} - {self.fecha_valoracion} ({tipo})"




class Profile(models.Model):
    #Informacion personal
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    contrasena = models.CharField(max_length=255, blank=True, null=True, verbose_name="Actual contraseña de usuario")
    sucursales = models.ForeignKey(Sucursal,on_delete=models.CASCADE,related_name="sucursal33",null=True, blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, verbose_name="Foto Perfil")
    ruc = models.CharField(max_length=13, verbose_name="C.I Paciente", help_text="Ingrese C.I del Paciente",blank=True, null=True)
    nombre_paciente = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombres")
    apellidos_paciente = models.CharField(max_length=255, blank=True, null=True, verbose_name="Apellidos")
    nacionalidad = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nacionalidad")
    sexo = models.CharField(blank=True, null=True, max_length=120, choices=[("MASCULINO", "Masculino"), ("FEMENINO", "Femenino")], verbose_name="Sexo del Paciente")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")
    edad =  models.CharField(max_length=255, blank=True, null=True, verbose_name="Edad")
    institucion =  models.ForeignKey(
        Prospeccion,
        on_delete=models.CASCADE,
        related_name="instituciones2",null=True, blank=True
    )
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

    adjunto_autorizacion = models.FileField(upload_to='documentos/pacientes/autorizacion/', blank=True, null=True)
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
    MOTIVOS_RETIRO = [
        ('economico', 'Económico'),
        ('insatisfecho', 'Insatisfecho'),
        ('otro', 'Otro'),
    ]

    es_en_terapia = models.BooleanField(default=False, verbose_name="¿Ha estado en terapia?")
    es_retirado = models.BooleanField(default=False, verbose_name="¿Ha sido retirado?")
    es_alta = models.BooleanField(default=False, verbose_name="¿Tiene alta terapéutica?")
    es_pausa = models.BooleanField(default=False, verbose_name="¿Ha estado en pausa?")

    valorizacion_terapeutica = models.ForeignKey(
        ValoracionTerapia,
        on_delete=models.CASCADE,
        related_name="valoraciones_terapeuticas",
        verbose_name="Valoración Terapéutica", blank=True, null=True,
    )
    tipo_servicio = models.ForeignKey(
        'ServicioTerapeutico',
        on_delete=models.CASCADE,
        related_name='servicios_terapeuticos3',
        verbose_name="Servicio terapéutico",null=True, blank=True
    )

    certificado_inicio = models.FileField(
        upload_to='certificados/inicio/',
        blank=True,
        null=True,
        verbose_name="Certificado de inicio terapeutico"
    )

    certificado_final = models.FileField(
        upload_to='certificados/final/',
        blank=True,
        null=True,
        verbose_name="Certificado de alta terapeutica"
    )


    # Campos opcionales según estado
    fecha_retiro = models.DateField(null=True, blank=True)
    motivo_retiro = models.CharField(max_length=50, choices=MOTIVOS_RETIRO, null=True, blank=True)
    motivo_otro = models.CharField(max_length=255, null=True, blank=True, help_text="Especifique otro motivo (si aplica)")

    fecha_inicio = models.DateField(blank=True, null=True, verbose_name="Fecha de inicio de tratamiento")

    fecha_alta = models.DateField(null=True, blank=True,verbose_name="Fecha de terminación de tratamiento")
    fecha_pausa = models.DateField(null=True, blank=True)
    fecha_re_inicio = models.DateField(blank=True, null=True, verbose_name="Fecha de re inicio de tratamiento")


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
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal4",null=True, blank=True
    )


    # NUEVOS CAMPOS BOOLEANOS DE ESTADO DE PAGO
    al_dia = models.BooleanField(default=False, verbose_name="Pago al día")
    pendiente = models.BooleanField(default=False, verbose_name="Pago pendiente")
    vencido = models.BooleanField(default=False, verbose_name="Pago vencido")

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=True, verbose_name="Paciente")
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
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal5",null=True, blank=True
    )
    servicio =  models.ForeignKey(
        'ServicioTerapeutico',
        on_delete=models.CASCADE,
        related_name='servicios_terapeuticos4',
        verbose_name="Servicio terapéutico",null=True, blank=True
    )
    ruc = models.CharField(max_length=13, verbose_name="R.U.C de facturación", help_text="Ingrese RUC de facturación",blank=True, null=True)
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
        verbose_name_plural = "Ordenes de Pago"
        verbose_name = "Orden de Pago "

    def __str__(self):
        return f"Pagos de servicio Paciente: {self.cliente.first_name}"

    #def save(self, *args, **kwargs):
        # Limpiar todos los estados primero
        #self.al_dia = False
        #self.pendiente = False
        #self.vencido = False

        # Determinar cuál activar
       # if self.fecha_emision_factura and self.fecha_vencimiento:
         #   diferencia = (self.fecha_vencimiento - self.fecha_emision_factura).days
         #   if self.fecha_pago:
         #       self.al_dia = True
        #    elif diferencia < 30:
       #         self.pendiente = True
      #      else:
     #           self.vencido = True

    #    super().save(*args, **kwargs)


class Cita(models.Model):
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='citas_creadas',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='citas_recibidas',
        on_delete=models.CASCADE
    )
    sucursal = models.ForeignKey(
        'Sucursal',
        on_delete=models.CASCADE,
        related_name="sucursal8",
        null=True,
        blank=True
    )
    fecha = models.DateTimeField()
    fecha_final = models.DateTimeField(null=True, blank=True)

    TIPO_CITA_CHOICES = [
        ('administrativa', 'Administrativa'),
        ('terapeutica', 'Terapéutica'),
        ('particular', 'Particular'),
        ('urgente', 'Urgente'),
    ]
    tipo_cita = models.CharField(
        max_length=20,
        choices=TIPO_CITA_CHOICES,
        default='terapeutica',
        verbose_name="Categoría de Cita"
    )

    motivo = models.CharField(max_length=255)
    notas = models.TextField(blank=True, null=True)

    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Asignar perfil de paciente",
        related_name='Asignar_perfil_de_paciente'
    )

    profile_terapeuta = models.ForeignKey(
        'Perfil_Terapeuta',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Asignar perfil de terapeuta",
        related_name='Asignar_perfil_de_terapeuta'
    )

    # Representación del estado con booleanos
    pendiente = models.BooleanField(default=True, verbose_name="¿Pendiente?")
    confirmada = models.BooleanField(default=False, verbose_name="¿Confirmada?")
    cancelada = models.BooleanField(default=False, verbose_name="¿Cancelada?")

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Administrativos / Ingreso de Cita"
        verbose_name_plural = "Registros Administrativos / Ingreso de Citas"

    @property
    def estado(self):
        if self.confirmada:
            return "Confirmada"
        if self.pendiente:
            return "Pendiente"
        if self.cancelada:
            return "Cancelada"
        return "Sin estado"

    def __str__(self):
        return f"{self.creador} → {self.destinatario} ({self.fecha.strftime('%d/%m/%Y %H:%M')})"

    def clean(self):
        # Esta validación se refleja en el formulario del admin
        estados = ['pendiente', 'confirmada', 'cancelada']
        seleccionados = [estado for estado in estados if getattr(self, estado)]

        if len(seleccionados) > 1:
            raise ValidationError("Solo un estado puede estar activo a la vez: pendiente, confirmada o cancelada.")




    

    class Meta:
        
        ordering = ['-fecha']
        verbose_name_plural = "Citas Agendadas"
        verbose_name = "Cita Agendada"

def __str__(self):
    return f"{self.creador} → {self.destinatario} ({self.fecha.strftime('%d/%m/%Y %H:%M')})"


class tareas(models.Model):
    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='paciente_asigna_tarea',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    cita_terapeutica_asignada = models.OneToOneField(Cita, on_delete=models.CASCADE, verbose_name="Elija la cita correspondiente a esta sesion de terapia", null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    terapeuta = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='terapeuta_asiga_tarea',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    titulo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Título de la tarea") 
    fecha_envio = models.DateField(blank=True, null=True, verbose_name="Fecha de envio de tarea")
    fecha_entrega = models.DateField(blank=True, null=True, verbose_name="Fecha de entrega de tarea")
    material_adjunto =  models.FileField(upload_to='materiales/%Y/%m/%d/', blank=True, verbose_name="Material adjunto")
    media_terapia =  models.FileField(upload_to='Videos/%Y/%m/%d/', blank=True, verbose_name="Contenido Multimedia de Terapia")
    descripcion_tarea = models.TextField(blank=True, null=True,verbose_name="Descripción de la tarea")
    realizada = models.BooleanField(default=False, verbose_name="¿Paciente realizó la tarea?")
    tarea_no_realizada = models.BooleanField(default=False, verbose_name="¿Paciente Culminó la Terapia ?")
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal6",null=True, blank=True
    )




    class Meta:
        ordering = ['paciente']
        verbose_name_plural = "Tareas Asignadas"
        verbose_name = "Paciente/ Tareas"

    def __str__(self):
        return f"Tareas terapéuticas de {self.paciente.username}"



class TareaComentario(models.Model):
    tarea = models.ForeignKey('tareas', on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensaje = models.TextField(verbose_name="Comentario o actividad")
    archivo = models.FileField(upload_to='tareas_respuestas/%Y/%m/%d/', blank=True, null=True, verbose_name="Archivo adjunto")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha']
        verbose_name = "Revisar Tarea Terapeutica"
        verbose_name_plural = "Revisar Tareas Terapeuticas"

    def __str__(self):
        return f"Corregir Tarea  {self.autor.username} - {self.tarea.titulo}"
    


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
    receptor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mensajes_recibidos', on_delete=models.CASCADE, verbose_name="Destinatario")
    asunto = models.CharField(max_length=50, choices=ASUNTOS_CHOICES, default='Consulta')  
    cuerpo = RichTextField(blank=True, null=True)
    leido = models.BooleanField(default=False)
    creado = models.DateTimeField(default=timezone.now)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal7",null=True, blank=True
    )

    # ➕ Campo para vincular con Celery
    task_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID de la tarea de Celery asociada")
    task_status = models.CharField(max_length=50, blank=True, null=True, help_text="Estado de la tarea de Celery asociada")

    class Meta:
        ordering = ['-fecha_envio']
        verbose_name_plural = "Bandeja de entrada MEDDES®"
        verbose_name = "Notificaciones de  MEDDES®"

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






class AsistenciaTerapeuta(models.Model):
    terapeuta = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='asistencia_terapeutica',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
   

    fecha = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    evento = models.OneToOneField(Cita, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Cita Agendada")
    
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal2", null=True, blank=True
    )

    # Nuevos campos booleanos de asistencia
    asistire = models.BooleanField(default=False, verbose_name="¿Confirmo que asistiré?")
    no_asistire = models.BooleanField(default=False, verbose_name="¿Confirmo que no asistiré?")

    class Meta:
        unique_together = ('terapeuta', 'fecha', 'hora_entrada')
        ordering = ['-fecha', 'hora_entrada']

    def save(self, *args, **kwargs):
        if self.asistire and self.no_asistire:
            raise ValueError("Solo uno de los campos puede estar activo: 'asistire' o 'no_asistire'.")

        super().save(*args, **kwargs)







class ComentarioCita(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor.username} el {self.fecha_creacion}"


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

    minutos_empleados = models.PositiveIntegerField(default=0, verbose_name="Minutos Empleados")
    minutos_restantes = models.PositiveIntegerField(default=4320, editable=False, verbose_name="Minutos Restantes")

    class Meta:
        verbose_name = "Entrada de Bitácora"
        verbose_name_plural = "Bitácora de Desarrollo QND.0.3.0.2"
        ordering = ['-fecha']

    def __str__(self):
        return f"[{self.fecha.strftime('%Y-%m-%d')}] {self.titulo} - {self.autor.username}"

    def save(self, *args, **kwargs):
        if not self.fecha_entrega:
            self.fecha_entrega = (timezone.now() + timedelta(days=5)).date()

        # Calcula los minutos restantes antes de guardar
        TOTAL_MINUTOS = 4320
        self.minutos_restantes = max(TOTAL_MINUTOS - self.minutos_empleados, 0)

        super().save(*args, **kwargs)