from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from productos.models import Producto, Categoria
from pedidos.models import Pedido


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.rol == 'cliente':
                return redirect("panel_cliente")

            elif user.rol == 'mozo':
                return redirect("panel_mozo")

            elif user.rol == 'cajero':
                return redirect("panel_cajero")

            elif user.rol == 'admin' or user.is_superuser:
                return redirect("/admin/")

            else:
                messages.error(request, "Rol no válido.")
                return redirect("login")

        else:
            messages.error(request, "Usuario o contraseña incorrecta")

    return render(request, "login.html")


def panel_cliente(request):
    # Ya no bloqueamos por rol aquí, permitimos que cualquiera vea la carta
    # Especialmente para que el admin pueda probar el flujo QR sin error.
    
    categorias = Categoria.objects.filter(activa=True).prefetch_related('productos')
    mesa_numero = request.session.get('mesa_numero')
    mesa_id = request.session.get('mesa_id')
    
    # Obtener pedidos recientes
    if request.user.is_authenticated and request.user.rol == 'cliente':
        pedidos_recientes = Pedido.objects.filter(usuario=request.user).order_by('-fecha')[:5]
    elif mesa_id:
        # Para invitados: Solo mostrar consumo ACTIVO (que no esté pagado)
        # Una vez pagado, la mesa queda "limpia" para el siguiente cliente.
        pedidos_recientes = Pedido.objects.filter(mesa_id=mesa_id).exclude(estado='pagado').order_by('-fecha')
    else:
        pedidos_recientes = []
    
    return render(request, "panel_cliente.html", {
        "categorias": categorias,
        "mesa_numero": mesa_numero,
        "pedidos_recientes": pedidos_recientes
    })


@login_required
def panel_mozo(request):
    if request.user.rol not in ['mozo', 'admin']:
        return HttpResponseForbidden("No tienes permiso.")
    
    from mesas.models import Mesa
    mesas = Mesa.objects.filter(activa=True).order_by('numero')
    
    # El mozo ve pedidos que no han sido pagados
    pedidos_activos = Pedido.objects.exclude(estado='pagado').order_by('fecha')
    
    return render(request, "panel_mozo.html", {
        "pedidos": pedidos_activos,
        "mesas": mesas
    })

@login_required
def mozo_atender_mesa(request, mesa_id):
    if request.user.rol != 'mozo':
        return HttpResponseForbidden("No tienes permiso.")
    
    from mesas.models import Mesa
    mesa = get_object_or_404(Mesa, id=mesa_id)
    request.session['mesa_id'] = mesa.id
    request.session['mesa_numero'] = mesa.numero
    
    messages.success(request, f"Atendiendo Mesa {mesa.numero}")
    return redirect('panel_cliente')



from django.db.models import Sum
from django.utils import timezone

@login_required
def panel_cajero(request):
    if request.user.rol not in ['cajero', 'admin']:
        return HttpResponseForbidden("No tienes permiso.")
        
    # El cajero ve todos los pedidos que no han sido pagados para gestionar cobros
    pedidos_para_cobro = Pedido.objects.exclude(estado='pagado').order_by('mesa__numero')
    
    # Calcular total ventas del día
    hoy = timezone.now().date()
    total_dia = Pedido.objects.filter(estado='pagado', fecha__date=hoy).aggregate(Sum('total'))['total__sum'] or 0
    
    return render(request, "panel_cajero.html", {
        "pedidos": pedidos_para_cobro,
        "total_dia": total_dia
    })


def logout_view(request):
    logout(request)
    return redirect("login")


# --- VISTAS DEL CARRITO EN SESIÓN ---

def agregar_al_carrito(request, producto_id):
    # Permitimos a invitados y a cualquier usuario logueado (incluido admin para pruebas)
    # que agreguen productos si están en el panel de cliente.
    
    # Obtener el carrito de la sesión o crear uno vacío si no existe
    carrito = request.session.get('carrito', {})
    
    # Convertir producto_id a string porque las llaves de sesión en JSON deben ser strings
    id_str = str(producto_id)
    
    if id_str in carrito:
        carrito[id_str]['cantidad'] += 1
        carrito[id_str]['subtotal'] = carrito[id_str]['precio'] * carrito[id_str]['cantidad']
    else:
        producto = Producto.objects.get(id=producto_id)
        precio = float(producto.precio)
        carrito[id_str] = {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': precio,
            'cantidad': 1,
            'subtotal': precio,
            'imagen': producto.imagen.url if producto.imagen else None
        }
    
    request.session['carrito'] = carrito
    messages.success(request, f"Producto agregado al carrito.")
    return redirect("panel_cliente")


def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    
    return render(request, "carrito.html", {
        "carrito": carrito,
        "total": total
    })


def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    
    if id_str in carrito:
        del carrito[id_str]
        request.session['carrito'] = carrito
        messages.success(request, "Producto eliminado del carrito.")
        
    return redirect("ver_carrito")


def vaciar_carrito(request):
    request.session['carrito'] = {}
    messages.success(request, "Carrito vaciado.")
    return redirect("panel_cliente")