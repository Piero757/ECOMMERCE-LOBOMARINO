from django.contrib import admin

from .models import GalleryImage, ContactInfo, ContactMessage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "orden", "activo")
    list_filter = ("categoria", "activo")
    search_fields = ("titulo",)
    ordering = ("orden", "id")


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("direccion", "telefono", "email", "horario", "activo")
    list_filter = ("activo",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "telefono", "creado_en")
    search_fields = ("nombre", "correo", "telefono")
    readonly_fields = ("creado_en",)
