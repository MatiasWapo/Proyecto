# =============================================
# FORMULARIOS PARA LA APLICACIÓN DE CLIENTES
# =============================================
# Este archivo contiene los formularios personalizados para la gestión
# de clientes, asegurando que todos los campos se procesen correctamente.

from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Cliente

class ClienteForm(forms.ModelForm):
    """
    Formulario personalizado para crear y editar clientes.
    Incluye validación específica para el campo precio_botellon.
    """
    
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'direccion', 'telefono', 'precio_botellon']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-agua-blue focus:border-transparent transition-all duration-200',
                'placeholder': 'Nombre del cliente'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-agua-blue focus:border-transparent transition-all duration-200',
                'placeholder': 'Apellido del cliente'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-agua-blue focus:border-transparent transition-all duration-200 resize-none',
                'rows': 3,
                'placeholder': 'Dirección completa del cliente'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-agua-blue focus:border-transparent transition-all duration-200',
                'placeholder': 'Teléfono de contacto'
            }),
            'precio_botellon': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200',
                'step': '0.5',
                'min': '0',
                'placeholder': '2.50'
            })
        }

class ClienteEditForm(ClienteForm):
    """
    Formulario para editar clientes que incluye el campo activo.
    """
    
    class Meta(ClienteForm.Meta):
        fields = ['nombre', 'apellido', 'direccion', 'telefono', 'precio_botellon', 'activo']
        widgets = {
            **ClienteForm.Meta.widgets,
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer valor por defecto para precio_botellon
        if not self.instance.pk:  # Solo para nuevos clientes
            self.fields['precio_botellon'].initial = Decimal('2.50')
    
    def clean_precio_botellon(self):
        """
        Validación personalizada para el campo precio_botellon.
        Asegura que el valor sea válido y se procese correctamente.
        """
        precio = self.cleaned_data.get('precio_botellon')
        
        # Log para depuración
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"[DEBUG] clean_precio_botellon - precio original: {precio} (tipo: {type(precio)})")
        
        # Si el precio es None o vacío, usar el valor por defecto
        if precio is None or precio == '':
            precio = Decimal('2.50')
            logger.info(f"[DEBUG] Precio vacío, usando valor por defecto: {precio}")
        
        # Convertir a Decimal si es necesario
        if not isinstance(precio, Decimal):
            try:
                precio = Decimal(str(precio))
                logger.info(f"[DEBUG] Precio convertido a Decimal: {precio}")
            except (ValueError, TypeError) as e:
                logger.error(f"[DEBUG] Error convirtiendo precio: {e}")
                raise ValidationError('El precio debe ser un número válido.')
        
        # Validar que el precio sea positivo
        if precio < 0:
            raise ValidationError('El precio no puede ser negativo.')
        
        # Validar que el precio tenga máximo 2 decimales
        if precio.as_tuple().exponent < -2:
            raise ValidationError('El precio puede tener máximo 2 decimales.')
        
        logger.info(f"[DEBUG] Precio final validado: {precio}")
        return precio
    
    def clean(self):
        """
        Validación general del formulario.
        """
        cleaned_data = super().clean()
        
        # Log para depuración
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"[DEBUG] clean() - datos limpios: {cleaned_data}")
        
        return cleaned_data 