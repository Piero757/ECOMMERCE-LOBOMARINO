from django.urls import path
from . import views

urlpatterns = [
    path('mesa/<uuid:slug>/', views.atender_mesa, name='atender_mesa'),
    path('confirmar/', views.confirmar_pedido, name='confirmar_pedido'),
    path('pedido/<int:pedido_id>/confirmado/', views.pedido_confirmado, name='pedido_confirmado'),
    path('pedido/<int:pedido_id>/cuenta/', views.pedido_cuenta, name='pedido_cuenta'),
    path('pedido/<int:pedido_id>/estado/<str:nuevo_estado>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
]
