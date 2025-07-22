"""
WSGI config for water_delivery project.

Expone la variable WSGI application para servidores compatibles (gunicorn, uWSGI, etc).
"""

import os

from django.core.wsgi import get_wsgi_application

# Configuración del entorno y obtención de la aplicación WSGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water_delivery.settings')

application = get_wsgi_application()
