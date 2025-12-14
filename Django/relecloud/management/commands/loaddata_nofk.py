"""
Comando personalizado para cargar datos iniciales sin restricciones de foreign keys.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


class Command(BaseCommand):
    help = 'Carga datos iniciales deshabilitando temporalmente las foreign key constraints'

    def add_arguments(self, parser):
        parser.add_argument(
            'fixture',
            nargs='?',
            default='initial_data.json',
            help='Nombre del archivo fixture a cargar'
        )

    def handle(self, *args, **options):
        fixture = options['fixture']
        
        self.stdout.write('Cargando datos iniciales con FK constraints deshabilitadas...')
        
        try:
            # Deshabilitar foreign key constraints
            with connection.cursor() as cursor:
                cursor.execute('PRAGMA foreign_keys = OFF;')
            
            # Cargar el fixture
            call_command('loaddata', fixture, verbosity=2, stdout=self.stdout)
            
            # Reactivar foreign key constraints
            with connection.cursor() as cursor:
                cursor.execute('PRAGMA foreign_keys = ON;')
            
            self.stdout.write(self.style.SUCCESS('✓ Datos cargados exitosamente'))
            
        except Exception as e:
            # Asegurar que las FK constraints se reactiven incluso si hay error
            try:
                with connection.cursor() as cursor:
                    cursor.execute('PRAGMA foreign_keys = ON;')
            except:
                pass
            
            self.stdout.write(self.style.ERROR(f'✗ Error al cargar datos: {e}'))
            raise
