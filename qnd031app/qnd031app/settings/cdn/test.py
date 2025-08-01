import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configuración de la conexión
s3 = boto3.client(
    's3',
    endpoint_url='https://sfo3.digitaloceanspaces.com',
    aws_access_key_id='DO007H7JJQHPNFGY6Q9H',  # Tu access key
    aws_secret_access_key='3xM8QodrbKAtmXjV3ryk8AdgqxkHG+AF6fcku2Qthg0',  # Tu secret key
)

# Intentamos subir un archivo de prueba
try:
    s3.upload_file('test2.txt', 'qnd-static', 'test2.txt')
    print("Archivo subido correctamente a DigitalOcean Spaces.")
except (NoCredentialsError, PartialCredentialsError) as e:
    print("Error de credenciales:", e)
except Exception as e:
    print(f"Error al subir el archivo: {e}")
