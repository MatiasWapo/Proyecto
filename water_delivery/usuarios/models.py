from django.db import models
from django.contrib.auth.models import AbstractUser 

class Usuario(AbstractUser ):
    es_empresa = models.BooleanField(default=False)
    es_conductor = models.BooleanField(default=False)
    camion_asignado = models.CharField(max_length=50, blank=True)

    
