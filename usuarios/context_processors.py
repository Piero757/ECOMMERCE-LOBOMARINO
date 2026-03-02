def global_context(request):
    carrito = request.session.get('carrito', {})
    count = 0
    for item in carrito.values():
        count += item.get('cantidad', 0)
    
    return {
        'carrito_count': count,
        'mesa_id': request.session.get('mesa_id'),
        'mesa_numero': request.session.get('mesa_numero'),
    }
