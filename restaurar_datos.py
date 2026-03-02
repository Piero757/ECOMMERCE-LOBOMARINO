import django
import os
import uuid
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario
from productos.models import Categoria, Producto
from mesas.models import Mesa
from django.contrib.auth import authenticate

# 1. Crear Superusuario
if not Usuario.objects.filter(username='Piero').exists():
    Usuario.objects.create_superuser('Piero', 'piero@example.com', 'Piero12345', rol='admin')
    print("Superusuario 'Piero' creado (pass: Piero12345)")

# 2. Crear Usuarios de Prueba
usuarios_prueba = [
    {'username': 'prueba_cliente', 'password': 'lobo1234', 'rol': 'cliente'},
    {'username': 'prueba_mozo',    'password': 'lobo1234', 'rol': 'mozo'},
    {'username': 'prueba_cajero',  'password': 'lobo1234', 'rol': 'cajero'},
]

for datos in usuarios_prueba:
    if not Usuario.objects.filter(username=datos['username']).exists():
        Usuario.objects.create_user(
            username=datos['username'],
            password=datos['password'],
            rol=datos['rol']
        )
        print(f"Usuario '{datos['username']}' creado.")

# 3. Crear Categorías y Productos
cat_ceviche, _ = Categoria.objects.get_or_create(nombre='Ceviches')
cat_bebida, _ = Categoria.objects.get_or_create(nombre='Bebidas')

if not Producto.objects.filter(nombre='Ceviche Clásico').exists():
    Producto.objects.create(
        nombre='Ceviche Clásico',
        descripcion='Pescado fresco marinado en limón, ají y sal.',
        precio=35.00,
        categoria=cat_ceviche,
        tipo_envio='cocina'
    )
    print("Producto 'Ceviche Clásico' creado.")

if not Producto.objects.filter(nombre='Inca Kola').exists():
    Producto.objects.create(
        nombre='Inca Kola',
        descripcion='Gaseosa nacional de 500ml.',
        precio=5.00,
        categoria=cat_bebida,
        tipo_envio='barra'
    )
    print("Producto 'Inca Kola' creado.")

# 4. Crear Mesas
for i in range(1, 6):
    Mesa.objects.get_or_create(numero=i)
print("Mesas 1 a 5 creadas.")
