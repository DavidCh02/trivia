import os
import django
from django.core.management import call_command

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()

# Ejecuta las migraciones
call_command('migrate')
