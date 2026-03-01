from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'tipo_envio', 'activo')
    list_filter = ('categoria', 'tipo_envio', 'activo')
    search_fields = ('nombre', 'descripcion')