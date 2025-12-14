#!/bin/bash

# Script de inicio para Azure App Service
# Ejecuta migraciones y luego inicia gunicorn

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Iniciando gunicorn..."
gunicorn --bind=0.0.0.0 --timeout 600 project.wsgi
