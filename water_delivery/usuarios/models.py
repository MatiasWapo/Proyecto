from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.hashers import make_password

class Usuario(AbstractUser):
    # Constantes para tipos de usuario
    EMPRESA = 'empresa'
    CONDUCTOR = 'conductor'
    TIPO_USUARIO_CHOICES = [
        (EMPRESA, 'Empresa'),
        (CONDUCTOR, 'Conductor'),
    ]
    def save(self, *args, **kwargs):
    # Versión alternativa sin django-dirtyfields
        if self.pk:  # Solo para instancias existentes
            original = Usuario.objects.get(pk=self.pk)
            if (self.respuesta_1.lower().strip() != original.respuesta_1.lower().strip() or 
                self.respuesta_2.lower().strip() != original.respuesta_2.lower().strip()):
                self.respuesta_1 = make_password(self.respuesta_1.lower().strip())
                self.respuesta_2 = make_password(self.respuesta_2.lower().strip())
        else:  # Para nuevas instancias
            self.respuesta_1 = make_password(self.respuesta_1.lower().strip())
            self.respuesta_2 = make_password(self.respuesta_2.lower().strip())
    
        super().save(*args, **kwargs)
    
    # Preguntas fijas de seguridad (simplificado)
    PREGUNTA_CHOICES = [
        ('ciudad', '¿En qué ciudad naciste?'),
        ('comida', '¿Cuál es tu comida favorita?'),
    ]

    # Campos del modelo
    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO_CHOICES,
        default=CONDUCTOR
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
    
    # Preguntas de seguridad (nombres más consistentes)
    pregunta_1 = models.CharField(
        max_length=20,
        choices=PREGUNTA_CHOICES,
        default='ciudad',
        verbose_name="Pregunta de seguridad 1"
    )
    
    respuesta_1 = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        verbose_name="Respuesta 1",
        default='respuesta_default_1'  # AÑADIDO valor por defecto
    )
    
    pregunta_2 = models.CharField(
        max_length=20,
        choices=PREGUNTA_CHOICES,
        default='comida',
        verbose_name="Pregunta de seguridad 2"
    )
    
    respuesta_2 = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        verbose_name="Respuesta 2",
        default='respuesta_default_2'  # AÑADIDO valor por defecto
    )

    class Meta:
        verbose_name = "Usuario del sistema"
        verbose_name_plural = "Usuarios del sistema"

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"