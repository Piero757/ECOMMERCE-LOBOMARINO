import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario
from django.contrib.auth import authenticate

# Usuarios de prueba a crear (eliminamos antes si ya existen para limpiar)
usuarios_prueba = [
    {'username': 'prueba_cliente', 'password': 'lobo1234', 'rol': 'cliente'},
    {'username': 'prueba_mozo',    'password': 'lobo1234', 'rol': 'mozo'},
    {'username': 'prueba_cajero',  'password': 'lobo1234', 'rol': 'cajero'},
]

print("=== Creando usuarios de prueba ===")
for datos in usuarios_prueba:
    Usuario.objects.filter(username=datos['username']).delete()
    u = Usuario.objects.create_user(
        username=datos['username'],
        password=datos['password'],
        rol=datos['rol']
    )
    # Verificar que autentica
    auth = authenticate(username=datos['username'], password=datos['password'])
    estado = "OK" if auth else "FALLO"
    print(f"  [{estado}] username={u.username} | rol={u.rol} | password={datos['password']}")

print()
print("=== Todos los usuarios en BD ===")
for u in Usuario.objects.all():
    print(f"  username={u.username} | rol={u.rol} | is_active={u.is_active}")
