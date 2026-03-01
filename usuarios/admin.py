from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Campos que se muestran al EDITAR un usuario existente
    fieldsets = UserAdmin.fieldsets + (
        ('Rol del usuario', {'fields': ('rol',)}),
    )
    # Campos que se muestran al CREAR un usuario nuevo
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol del usuario', {'fields': ('rol',)}),
    )
    list_display = ('username', 'email', 'rol', 'is_active', 'is_staff')
    list_filter = ('rol', 'is_active', 'is_staff')