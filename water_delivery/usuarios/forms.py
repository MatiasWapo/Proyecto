from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator, RegexValidator  # Añade RegexValidator aquí
from django.core.exceptions import ValidationError
from .models import Usuario
import re
from django.contrib.auth.password_validation import validate_password

class CustomUserCreationForm(UserCreationForm):
    telefono = forms.CharField(
        max_length=20,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message="Formato de teléfono inválido. Use +584144770130 o 04144770130"
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 pl-12',
            'placeholder': 'Ej: +584144770130 o 04144770130'
        }),
        label='Teléfono'
    )
    
    direccion = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 pl-12 resize-none',
            'placeholder': 'Ingresa tu dirección completa...',
            'rows': 3
        }),
        label='Dirección'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 pl-12',
            'placeholder': 'tu@email.com'
        }),
        label='Correo Electrónico'
    )
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password1', 'password2', 'telefono', 'direccion',
            'tipo_usuario', 'camion_asignado'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        common_attrs = {
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 pl-12'
        }
        
        self.fields['username'].widget.attrs.update({
            **common_attrs,
            'placeholder': 'Elige tu nombre de usuario'
        })
        self.fields['password1'].widget.attrs.update({
            **common_attrs,
            'placeholder': 'Crea una contraseña segura',
            'class': common_attrs['class'] + ' pr-12'
        })
        self.fields['password2'].widget.attrs.update({
            **common_attrs,
            'placeholder': 'Confirma tu contraseña',
            'class': common_attrs['class'] + ' pr-12'
        })
        
        if 'tipo_usuario' in self.fields:
            self.fields['tipo_usuario'].widget.attrs.update({
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200'
            })
            
        if 'camion_asignado' in self.fields:
            self.fields['camion_asignado'].widget.attrs.update({
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200'
            })
        
        for field in ['username', 'password1', 'password2']:
            self.fields[field].help_text = None
        
        self.fields['username'].label = 'Nombre de Usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar Contraseña'
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("El nombre de usuario es obligatorio")
        if len(username) < 4:
            raise ValidationError("El nombre de usuario debe tener al menos 4 caracteres")
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError("El nombre de usuario solo puede contener letras, números y los caracteres @/./+/-/_")
        return username
    
class RecuperacionForm(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        })
    )

class PreguntasSeguridadForm(forms.Form):
    nueva_password = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Ingresa tu nueva contraseña'
        }),
        validators=[
            MinLengthValidator(8, message="La contraseña debe tener al menos 8 caracteres"),
            RegexValidator(
                regex='^(?=.*[A-Za-z])(?=.*\d)',
                message="La contraseña debe contener letras y números"
            )
        ]
    )
    confirmar_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Confirma tu nueva contraseña'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_password = cleaned_data.get('nueva_password')
        confirmar_password = cleaned_data.get('confirmar_password')

        if nueva_password and confirmar_password and nueva_password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        
        return cleaned_data

class EmailForm(forms.Form):
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'tu@ejemplo.com'
        })
    )
    
class ResetPasswordForm(forms.Form):
    nueva_password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 pl-12',
            'placeholder': 'Ingresa tu nueva contraseña'
        }),
        validators=[
            MinLengthValidator(8, message="La contraseña debe tener al menos 8 caracteres"),
            RegexValidator(
                regex='^(?=.*[A-Za-z])(?=.*\d)',
                message="La contraseña debe contener letras y números"
            )
        ]
    )
    confirmar_password = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 pl-12',
            'placeholder': 'Confirma tu nueva contraseña'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_password = cleaned_data.get("nueva_password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if nueva_password and confirmar_password and nueva_password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden")

        try:
            validate_password(nueva_password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)

        return cleaned_data