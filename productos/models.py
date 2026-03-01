from django.db import models

class Producto(models.Model):

    CATEGORIA_CHOICES = (
        ('ceviche', 'Ceviches'),
        ('caliente', 'Platos Calientes'),
        ('bebida', 'Bebidas'),
        ('postre', 'Postres'),
    )

    TIPO_ENVIO = (
        ('cocina', 'Cocina'),
        ('barra', 'Barra'),
    )

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    activo = models.BooleanField(default=True)
    tipo_envio = models.CharField(max_length=20, choices=TIPO_ENVIO)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre