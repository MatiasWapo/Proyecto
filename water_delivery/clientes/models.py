from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    debe_total = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Despacho(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad_botellones = models.IntegerField()
    entregado = models.BooleanField(default=False)
    notas = models.TextField(blank=True, null=True)
    
    # REMOVEMOS el save() personalizado para evitar duplicación
    def __str__(self):
        return f"Despacho a {self.cliente} - {self.cantidad_botellones} botellones"
