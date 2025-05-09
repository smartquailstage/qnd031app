import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from usuarios.models import Prospeccion


class Command(BaseCommand):
    help = "Importa datos desde un archivo CSV al modelo Prospeccion"

    def handle(self, *args, **kwargs):
        # Cargar variables de entorno
        BASE_DIR = Path(settings.BASE_DIR)
        ENV_FILE_PATH = BASE_DIR / ".env_stage"
        load_dotenv(dotenv_path=ENV_FILE_PATH)

        csv_path = os.getenv('EXCEL_PATH')  # Reutilizamos EXCEL_PATH para CSV

        if not csv_path:
            raise CommandError("❌ La variable de entorno EXCEL_PATH no está definida en .env_stage.")

        if not os.path.exists(csv_path):
            raise CommandError(f"❌ No se encontró el archivo CSV en: {csv_path}")

        self.stdout.write(f"📄 Cargando archivo CSV desde: {csv_path}")

        # Leer CSV (ajusta encoding si es necesario)
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(csv_path, encoding='latin1')  # Alternativa si utf-8 falla

        # Eliminar columnas sin nombre (por errores comunes al exportar desde Excel)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Verificar columnas obligatorias
        campos_requeridos = ['DISTRITO', 'NOMBRE DE LA INSTITUCIÓN']
        for campo in campos_requeridos:
            if campo not in df.columns:
                raise CommandError(f"❌ Falta columna obligatoria en el CSV: '{campo}'")

        nuevos, actualizados, omitidos = 0, 0, 0

        for _, row in df.iterrows():
            if pd.isnull(row.get('DISTRITO')) or pd.isnull(row.get('NOMBRE DE LA INSTITUCIÓN')):
                omitidos += 1
                self.stdout.write(self.style.WARNING(f"⚠️ Fila incompleta omitida: {row.to_dict()}"))
                continue

            try:
                obj, created = Prospeccion.objects.update_or_create(
                    nombre_institucion=row.get('NOMBRE DE LA INSTITUCIÓN'),
                    defaults={
                        'distrito': row.get('DISTRITO'),
                        'provincia': row.get('PROVINCIA'),
                        'zona': row.get('ZONA'),
                        'sostenimiento': row.get('SOSTENIMIENTO'),
                        'estado': row.get('ESTADO'),
                        'telefono': row.get('TELEFONO'),
                        'sector': row.get('SECTOR'),
                        'direccion': row.get('DIRECCION'),
                        'tl_nombre_contacto': row.get('TERAPIA DE LENGUAJE NOMBRE DE CONTACTO'),
                        'tl_cargo_contacto': row.get('TERAPIA DE LENGUAJE CARGO CONTACTO'),
                        'tl_email': row.get('TERAPIA DE LENGUAJE EMAIL'),
                        'tl_proceso_realizado': row.get('TERAPIA DE LENGUAJE PROCESO REALIZADO'),
                        'tl_responsable': row.get('TERAPIA DE LENGUAJE RESPONSABLE'),
                        'tl_fecha_contacto': pd.to_datetime(row.get('TERAPIA DE LENGUAJE FECHA DE CONTACTO'), errors='coerce'),
                        'tl_observaciones': row.get('TL GENERAL OBSERVACIONES'),
                        'tl_fecha_proximo_contacto': pd.to_datetime(row.get('TL FECHA PROXIMO CONTACTO'), errors='coerce'),
                        'psicologia_email': row.get('PSICOLOGIA EMAIL'),
                        'psicologia_observaciones': row.get('P GENERAL OBSERVACIONES'),
                        'psicologia_fecha_proximo_contacto': pd.to_datetime(row.get('P FECHA PROXIMO CONTACTO'), errors='coerce'),
                        'vya_observacion': row.get('VYA OBSERVACIÓN'),
                        'vya_observaciones': row.get('VYA GENERAL OBSERVACIONES'),
                        'vya_fecha_proximo_contacto': pd.to_datetime(row.get('VYA FECHA PROXIMO CONTACTO'), errors='coerce'),
                    }
                )
                if created:
                    nuevos += 1
                else:
                    actualizados += 1
            except Exception as e:
                omitidos += 1
                self.stdout.write(self.style.ERROR(f"❌ Error al importar fila: {e}"))

        self.stdout.write(self.style.SUCCESS(
            f"✅ Importación terminada: {nuevos} nuevos, {actualizados} actualizados, {omitidos} filas omitidas."
        ))
