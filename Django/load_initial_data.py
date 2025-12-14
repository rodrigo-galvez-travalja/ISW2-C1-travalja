#!/usr/bin/env python
"""
Script para cargar datos iniciales con foreign key constraints deshabilitadas.
Esto es necesario para SQLite cuando hay referencias circulares o complejas.
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def load_fixture_without_fk_checks():
    """Carga el fixture deshabilitando temporalmente las foreign key constraints."""
    cursor = connection.cursor()
    
    try:
        # Deshabilitar las comprobaciones de foreign keys
        cursor.execute('PRAGMA foreign_keys = OFF;')
        
        print("Cargando datos iniciales con FK constraints deshabilitadas...")
        
        # Cargar el fixture
        call_command('loaddata', 'initial_data.json', verbosity=2)
        
        # Reactivar las comprobaciones de foreign keys
        cursor.execute('PRAGMA foreign_keys = ON;')
        
        print("✓ Datos cargados exitosamente")
        
    except Exception as e:
        print(f"✗ Error al cargar datos: {e}")
        # Asegurarse de reactivar las FK constraints incluso si hay error
        cursor.execute('PRAGMA foreign_keys = ON;')
        sys.exit(1)
    finally:
        cursor.close()

if __name__ == '__main__':
    load_fixture_without_fk_checks()
