import uuid
from django.db import models

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    activa = models.BooleanField(default=True)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_codigo = models.ImageField(upload_to='qr_mesas/', blank=True, null=True)

    def __str__(self):
        return f"Mesa {self.numero}"