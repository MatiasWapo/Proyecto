from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Usuario(AbstractUser):
    EMPRESA = 'empresa'
    CONDUCTOR = 'conductor'
    TIPO_USUARIO_CHOICES = [
        (EMPRESA, 'Empresa'),
        (CONDUCTOR, 'Conductor'),
        
    ]

    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO_CHOICES,
        default=CONDUCTOR
    )
    
    email = models.EmailField(
        verbose_name="Correo electrónico",
        unique=True,
        blank=False,
        null=False
    )
    
    token_recuperacion = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        unique=True
    )
    
    token_recuperacion_fecha = models.DateTimeField(
        blank=True,
        null=True
    )
    
    direccion = models.TextField(
        verbose_name="Dirección completa",
        default="Sin dirección registrada"
    )
    
    telefono = models.CharField(
        max_length=20,
        verbose_name="Teléfono de contacto",
        default="0000000000"
    )
    
    camion_asignado = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Camión asignado"
    )
    
        # Campos críticos con valores por defecto
    password = models.CharField(max_length=128, default='', verbose_name='password')
    last_login = models.DateTimeField(null=True, blank=True, default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    # Asegura que estos campos no sean nulos
    email = models.EmailField(verbose_name="Correo electrónico", unique=True, blank=False, default='')
    direccion = models.TextField(verbose_name="Dirección completa", default="Sin dirección registrada")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono de contacto", default="0000000000")

    class Meta:
        verbose_name = "Usuario del sistema"
        verbose_name_plural = "Usuarios del sistema"

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"