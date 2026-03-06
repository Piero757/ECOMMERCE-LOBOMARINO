from django.db import models


class GalleryImage(models.Model):
    CATEGORIA_CHOICES = [
        ("platos", "Platos"),
        ("ambiente", "Ambiente"),
        ("equipo", "Equipo"),
        ("ingredientes", "Ingredientes"),
        ("bebidas", "Bebidas"),
    ]

    titulo = models.CharField(max_length=150)
    categoria = models.CharField(
        max_length=20, choices=CATEGORIA_CHOICES, default="platos"
    )
    imagen = models.ImageField(upload_to="galeria/")
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Imagen de galería"
        verbose_name_plural = "Imágenes de galería"

    def __str__(self) -> str:
        return self.titulo


class ContactInfo(models.Model):
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=50)
    email = models.EmailField()
    horario = models.CharField(max_length=255)
    mapa_embed = models.TextField(
        blank=True,
        help_text="Código iframe o URL de mapa (opcional).",
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Información de contacto"
        verbose_name_plural = "Información de contacto"

    def __str__(self) -> str:
        return "Información de contacto"


class ContactMessage(models.Model):
    nombre = models.CharField(max_length=150)
    correo = models.EmailField()
    telefono = models.CharField(max_length=50, blank=True)
    mensaje = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"

    def __str__(self) -> str:
        return f"{self.nombre} - {self.correo}"
