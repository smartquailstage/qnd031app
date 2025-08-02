import os

# Accede a las variables de entorno para obtener las credenciales de AWS
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")  # Cambia si usas otro endpoint

# Parámetros de objetos S3 (ajustar según tus necesidades)
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400", 
    "ACL": "public-read"  # Cambia a 'private' si los archivos deben ser privados
}

# Establecer la ubicación de los archivos (asegurarse de que esté configurado en las variables de entorno)
AWS_LOCATION = os.environ.get("AWS_LOCATION", "static")  # Valor por defecto 'static' si no se encuentra

# Almacenamiento de archivos estáticos y medios usando las clases definidas en el proyecto
STATICFILES_STORAGE = os.environ.get("STATICFILES_STORAGE", "qnd031app.settings.cdn.backends.StaticRootS3BotoStorage")
MEDIA_STORAGE = os.environ.get("MEDIA_STORAGE", "qnd031app.settings.cdn.backends.MediaRootS3BotoStorage")

# Configuración de URL de los archivos estáticos
STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/'

# Opcionalmente, también se puede configurar la URL para los medios
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/media/'
