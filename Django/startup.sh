#!/bin/bash

# Script de inicio para Azure App Service
# Ejecuta migraciones, carga datos iniciales y luego inicia gunicorn

echo "Ejecutando migraciones..." 
python manage.py migrate --noinput

echo "Cargando datos iniciales..."
python load_initial_data.py || echo "No hay datos iniciales o ya están cargados"
