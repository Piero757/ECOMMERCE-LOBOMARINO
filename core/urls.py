from django.urls import path
from . import views

urlpatterns = [
    path("galeria/", views.galeria_view, name="galeria"),
    path("contacto/", views.contacto_view, name="contacto"),
]
