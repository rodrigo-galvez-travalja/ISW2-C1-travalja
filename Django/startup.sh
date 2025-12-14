#!/bin/bash

# Script de inicio para Azure App Service
# Ejecuta migraciones, carga datos iniciales y luego inicia gunicorn

echo "Ejecutando migraciones..." 
python manage.py migrate --noinput

echo "Cargando datos iniciales..."
python manage.py loaddata initial_data.json --ignorenonexistent || echo "No hay datos iniciales o ya están cargados"

echo "Iniciando gunicorn..."
gunicorn --bind=0.0.0.0 --timeout 600 project.wsgi
