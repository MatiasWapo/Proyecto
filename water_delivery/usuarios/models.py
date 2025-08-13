# =============================================
# MODELO DE USUARIO PERSONALIZADO
# =============================================
# Este archivo define el modelo de usuario extendido para la app de usuarios.
# Permite distinguir entre usuarios tipo empresa y conductor, y almacena datos
# adicionales como dirección, teléfono, camión asignado y recuperación de contraseña.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Usuario(AbstractUser):
    """
    Modelo personalizado de usuario para el sistema Water Delivery.
    Permite distinguir entre empresa y conductor, y añade campos extra.
    """
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
    )  # Tipo de usuario: empresa o conductor
    
    email = models.EmailField(
        verbose_name="Correo electrónico",
        unique=True,
        blank=False,
        null=False
    )  # Correo electrónico único
    
    token_recuperacion = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        unique=True
    )  # Token para recuperación de contraseña
    
    token_recuperacion_fecha = models.DateTimeField(
        blank=True,
        null=True
    )  # Fecha de generación del token
    
    direccion = models.TextField(
        verbose_name="Dirección completa",
        default="Sin dirección registrada"
    )  # Dirección del usuario
    
    telefono = models.CharField(
        max_length=20,
        verbose_name="Teléfono de contacto",
        default="0000000000"
    )  # Teléfono del usuario
    
    camion_asignado = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Camión asignado"
    )  # Camión asignado al conductor (opcional)

    class Meta:
        verbose_name = "Usuario del sistema"
        verbose_name_plural = "Usuarios del sistema"

    def __str__(self):
        """Representación legible del usuario"""
        return f"{self.username} ({self.get_tipo_usuario_display()})"