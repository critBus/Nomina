import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings

from django_reportbroD.models import ReportDefinition

class Command(BaseCommand):
    help = 'Exporta todos los reportes a archivos JSON en una carpeta específica'

    def add_arguments(self, parser):
        parser.add_argument(
            'folder_name',
            type=str,
            help='Nombre de la carpeta donde se guardarán los reportes'
        )

    def handle(self, *args, **options):
        folder_name = options['folder_name']
        base_dir = settings.BASE_DIR
        export_dir = os.path.join(base_dir, folder_name)

        # Crear el directorio si no existe
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
            self.stdout.write(self.style.SUCCESS(f'Directorio {export_dir} creado'))

        # Obtener todos los reportes
        reports = ReportDefinition.objects.all()
        
        if not reports.exists():
            self.stdout.write(self.style.WARNING('No hay reportes para exportar'))
            return

        # Exportar cada reporte
        for report in reports:
            file_path = os.path.join(export_dir, f'{report.name}.json')
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(report.to_dict(), f, ensure_ascii=False, indent=4)
                self.stdout.write(self.style.SUCCESS(f'Reporte {report.name} exportado correctamente'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al exportar {report.name}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Proceso de exportación completado')) 