# =============================================
# MODELOS DE CLIENTE, DESPACHO Y PAGO
# =============================================
# Este archivo define las estructuras de datos principales para la app de clientes:
# Cliente: información y saldo del cliente.
# Despacho: registro de entregas de botellones.
# Pago: registro de abonos realizados por el cliente.

from django.db import models

class Cliente(models.Model):
    """
    Modelo que representa a un cliente de la empresa.
    Guarda datos personales, dirección, teléfono, estado y saldo.
    """
    nombre = models.CharField(max_length=100)  # Nombre del cliente
    apellido = models.CharField(max_length=100)  # Apellido del cliente
    direccion = models.TextField()  # Dirección completa
    telefono = models.CharField(max_length=20)  # Teléfono de contacto
    activo = models.BooleanField(default=True)  # Si el cliente está activo
    debe_total = models.IntegerField(default=0)  # Deuda total acumulada
    precio_botellon = models.DecimalField(max_digits=5, decimal_places=2, default=2.5)  # Precio por botellón
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Saldo actual del cliente
    
    def __str__(self):
        """Representación legible del cliente"""
        return f"{self.nombre} {self.apellido}"

class Despacho(models.Model):
    """
    Modelo que representa un despacho (entrega) de botellones a un cliente.
    Guarda cantidad, fecha, notas, precio y estado de entrega.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Cliente asociado
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha y hora del despacho
    cantidad_botellones = models.IntegerField()  # Cantidad de botellones entregados
    entregado = models.BooleanField(default=False)  # Si el despacho fue entregado
    notas = models.TextField(blank=True, null=True)  # Notas adicionales
    precio_unitario = models.DecimalField(max_digits=5, decimal_places=2, default=2.5)  # Precio por botellón
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total del despacho
    
    def __str__(self):
        """Representación legible del despacho"""
        return f"Despacho a {self.cliente} - {self.cantidad_botellones} botellones"

class Pago(models.Model):
    """
    Modelo que representa un pago realizado por un cliente.
    Guarda monto, fecha, observaciones y cliente asociado.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pagos')  # Cliente que paga
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha y hora del pago
    monto = models.DecimalField(max_digits=10, decimal_places=2)  # Monto del pago
    observaciones = models.TextField(blank=True, null=True)  # Observaciones adicionales
    def __str__(self):
        """Representación legible del pago"""
        return f"Pago de {self.monto} $ de {self.cliente} el {self.fecha.strftime('%d/%m/%Y')}"
