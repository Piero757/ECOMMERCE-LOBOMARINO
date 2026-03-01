from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from productos.models import Producto


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


@login_required
def panel_cliente(request):
    if request.user.rol != 'cliente':
        return HttpResponseForbidden("No tienes permiso.")
    productos = Producto.objects.filter(activo=True)
    return render(request, "panel_cliente.html", {"productos": productos})


@login_required
def panel_mozo(request):
    if request.user.rol != 'mozo':
        return HttpResponseForbidden("No tienes permiso.")
    return render(request, "panel_mozo.html")


@login_required
def panel_cajero(request):
    if request.user.rol != 'cajero':
        return HttpResponseForbidden("No tienes permiso.")
    return render(request, "panel_cajero.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# --- VISTAS DEL CARRITO EN SESIÓN ---

@login_required
def agregar_al_carrito(request, producto_id):
    if request.user.rol != 'cliente':
        return HttpResponseForbidden("Solo los clientes pueden comprar.")
    
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


@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    
    return render(request, "carrito.html", {
        "carrito": carrito,
        "total": total
    })


@login_required
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    
    if id_str in carrito:
        del carrito[id_str]
        request.session['carrito'] = carrito
        messages.success(request, "Producto eliminado del carrito.")
        
    return redirect("ver_carrito")


@login_required
def vaciar_carrito(request):
    request.session['carrito'] = {}
    messages.success(request, "Carrito vaciado.")
    return redirect("panel_cliente")