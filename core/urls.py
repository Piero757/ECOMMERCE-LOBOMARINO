from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin-panel/", views.panel_admin, name="panel_admin"),
    path("mozo-panel/", views.panel_mozo, name="panel_mozo"),
    path("cajero-panel/", views.panel_cajero, name="panel_cajero"),
    path("cliente-panel/", views.panel_cliente, name="panel_cliente"),
]
