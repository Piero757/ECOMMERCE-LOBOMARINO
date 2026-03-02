from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login_root"),
    path("login/", views.login_view, name="login"),
    path("cliente/", views.panel_cliente, name="panel_cliente"),
    path("mozo/", views.panel_mozo, name="panel_mozo"),
    path("cajero/", views.panel_cajero, name="panel_cajero"),
    path("logout/", views.logout_view, name="logout"),
    # Carrito
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/eliminar/<int:producto_id>/", views.eliminar_del_carrito, name="eliminar_del_carrito"),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('mozo/atender/<int:mesa_id>/', views.mozo_atender_mesa, name='mozo_atender_mesa'),
]