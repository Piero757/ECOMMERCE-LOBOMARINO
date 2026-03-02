from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):

    TIPO_ENVIO = (
        ('cocina', 'Cocina'),
        ('barra', 'Barra'),
    )

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    activo = models.BooleanField(default=True)
    tipo_envio = models.CharField(max_length=20, choices=TIPO_ENVIO)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre