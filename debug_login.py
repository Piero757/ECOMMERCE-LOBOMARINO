import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate
u = authenticate(username='Miler', password='lobo1234')
if u:
    print(f'Autenticacion EXITOSA: rol={u.rol}')
else:
    print('Autenticacion FALLO')
