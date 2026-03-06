from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import Pedido, DetallePedido
from productos.models import Producto
from mesas.models import Mesa


def atender_mesa(request, slug):
    """
    Vista que se usa cuando el cliente escanea el QR de la mesa.
    Solo guarda la mesa en sesión y redirige al inicio bonito.
    """
    mesa = get_object_or_404(Mesa, slug=slug, activa=True)
    request.session['mesa_id'] = mesa.id
    request.session['mesa_numero'] = mesa.numero

    return redirect('inicio_mesa')


def inicio_mesa(request):
    """
    Vista para el botón 'Inicio' del cliente.
    Muestra el landing con hero + secciones. Si hay mesa en sesión,
    la mostramos en un badge; si no, se ve genérico.
    """
    mesa = None
    mesa_id = request.session.get('mesa_id')
    if mesa_id:
        mesa = get_object_or_404(Mesa, id=mesa_id, activa=True)

    productos_destacados = Producto.objects.filter(activo=True)[:3]

    return render(
        request,
        'pedidos/bienvenida_mesa.html',
        {
            'mesa': mesa,
            'productos_destacados': productos_destacados,
        },
    )

from decimal import Decimal

def confirmar_pedido(request):
    # Permitimos que cualquiera con una mesa asignada confirme el pedido.
    # Especialmente para pruebas del staff/admin.
    
    carrito = request.session.get('carrito', {})
    mesa_id = request.session.get('mesa_id')
    
    if not carrito:
        messages.error(request, "El carrito está vacío.")
        return redirect('panel_cliente')
        
    if not mesa_id:
        messages.error(request, "Debe escanear un código QR de mesa primero.")
        return redirect('panel_cliente')

    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    # Buscar si ya existe un pedido activo para esta mesa (que no esté pagado)
    # IMPORTANTE: Se acumula en el mismo pedido mientras no esté con estado 'pagado'.
    # Esto incluye estados: 'pendiente', 'confirmado', 'preparando', 'listo', 'entregado', 'cuenta'.
    pedido = Pedido.objects.filter(mesa=mesa).exclude(estado='pagado').order_by('-fecha').first()
    
    if not pedido:
        # Si no hay pedido activo, creamos uno nuevo
        usuario_pedido = request.user if request.user.is_authenticated else None
        pedido = Pedido.objects.create(
            usuario=usuario_pedido,
            mesa=mesa,
            estado='pendiente',
            total=Decimal('0.00')
        )
    else:
        # Si el pedido estaba en 'cuenta', lo volvemos a 'pendiente' 
        # para que el mozo sepa que hay nuevas adiciones.
        if pedido.estado == 'cuenta':
            pedido.estado = 'pendiente'
            pedido.save()
    
    # Añadir o actualizar productos en el pedido
    total_adicional = Decimal('0.00')
    for key, item in carrito.items():
        producto = get_object_or_404(Producto, id=item['id'])
        # Convertimos el precio a Decimal para evitar errores de tipo con el total de la BD
        precio_decimal = Decimal(str(item['precio']))
        subtotal_item = precio_decimal * item['cantidad']
        total_adicional += subtotal_item
        
        # Verificar si el producto ya está en el detalle del pedido
        detalle, created = DetallePedido.objects.get_or_create(
            pedido=pedido,
            producto=producto,
            defaults={'cantidad': item['cantidad'], 'precio_unitario': precio_decimal}
        )
        
        if not created:
            # Si ya existía, sumamos la cantidad y actualizamos el precio por si cambió
            detalle.cantidad += item['cantidad']
            detalle.precio_unitario = precio_decimal
            detalle.save()
        
    # Actualizar el total general del pedido
    pedido.total += total_adicional
    pedido.save()
    
    # Vaciar carrito de la sesión
    request.session['carrito'] = {}
    
    messages.success(request, f"Se han añadido los productos a tu pedido.")
    return redirect('pedido_confirmado', pedido_id=pedido.id)


def pedido_confirmado(request, pedido_id):
    # Intentar obtener el pedido
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Seguridad básica para invitados: verificar que la mesa del pedido coincida con la de la sesión
    mesa_sesion_id = request.session.get('mesa_id')
    
    if request.user.is_authenticated:
        # Staff (Mozo, Cajero, Admin) siempre puede ver
        if request.user.rol in ['mozo', 'cajero', 'admin']:
            pass
        # Clientes solo sus propios pedidos
        elif request.user.rol == 'cliente' and pedido.usuario != request.user:
             return HttpResponseForbidden("No tienes permiso para ver este pedido.")
    else:
        # Si es invitado, validamos que la mesa coincida con su sesión actual
        if not mesa_sesion_id or pedido.mesa.id != mesa_sesion_id:
            return HttpResponseForbidden("No tienes permiso para ver este pedido.")

    # Simulación de tiempo: 20-30 min
    tiempo_estimado = "20-30 min"
    return render(request, 'pedidos/pedido_confirmado.html', {
        'pedido': pedido,
        'tiempo_estimado': tiempo_estimado
    })

def pedido_cuenta(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    # Seguridad básica
    mesa_sesion_id = request.session.get('mesa_id')
    if not request.user.is_authenticated:
        if not mesa_sesion_id or pedido.mesa.id != mesa_sesion_id:
            return HttpResponseForbidden("No tienes permiso.")
            
    return render(request, 'pedidos/gracias_visita.html', {'pedido': pedido})

def cambiar_estado_pedido(request, pedido_id, nuevo_estado):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    mesa_sesion_id = request.session.get('mesa_id')

    # Validación de permisos
    if request.user.is_authenticated:
        # El staff puede cambiar a cualquier estado
        if request.user.rol in ['mozo', 'cajero', 'admin']:
            pass
        # El cliente solo puede pedir su cuenta
        elif request.user.rol == 'cliente' and pedido.usuario == request.user and nuevo_estado == 'cuenta':
            pass
        else:
            return HttpResponseForbidden("No tienes permiso.")
    else:
        # Los invitados solo pueden pedir la cuenta si la mesa coincide
        if nuevo_estado == 'cuenta' and mesa_sesion_id and pedido.mesa.id == mesa_sesion_id:
            pass
        else:
            return HttpResponseForbidden("Debe iniciar sesión para realizar esta acción.")
    
    pedido.estado = nuevo_estado
    pedido.save()

    messages.success(request, f"Estado del pedido #{pedido.id} actualizado a {nuevo_estado}.")

    # Siempre que se pida la cuenta, mostrar la pantalla de agradecimiento,
    # sin importar si es cliente, invitado o staff probando el flujo.
    if nuevo_estado == 'cuenta':
        return redirect('pedido_cuenta', pedido_id=pedido.id)

    if request.user.is_authenticated:
        if request.user.rol == 'mozo':
            return redirect('panel_mozo')
        elif request.user.rol in ['cajero', 'admin']:
            return redirect('panel_cajero')
        else:
            return redirect('/admin/')

    return redirect('panel_cliente')
