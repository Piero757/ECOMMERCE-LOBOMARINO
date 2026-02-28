from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    
    ROL_CHOICES = (
        ('cliente', 'Cliente'),
        ('mozo', 'Mozo'),
        ('cajero', 'Cajero'),
        ('admin', 'Administrador'),
    )

    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente')

    def __str__(self):
        return f"{self.username} - {self.rol}"