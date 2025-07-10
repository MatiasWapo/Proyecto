from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from .models import Usuario


class CustomUserCreationForm(UserCreationForm):
    telefono = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 pl-12',
            'placeholder': 'Ej: +1 (555) 123-4567'
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
    
    pregunta_1 = forms.ChoiceField(
        choices=Usuario.PREGUNTA_CHOICES,
        initial='ciudad',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
        }),
        label='Primera Pregunta de Seguridad'
    )
    
    respuesta_1 = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 pl-12',
            'placeholder': 'Tu respuesta...'
        }),
        validators=[MinLengthValidator(2)],
        label='Respuesta'
    )
    
    pregunta_2 = forms.ChoiceField(
        choices=Usuario.PREGUNTA_CHOICES,
        initial='comida',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
        }),
        label='Segunda Pregunta de Seguridad'
    )
    
    respuesta_2 = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 pl-12',
            'placeholder': 'Tu respuesta...'
        }),
        validators=[MinLengthValidator(2)],
        label='Respuesta'
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'password1', 'password2', 'telefono', 'direccion',
            'tipo_usuario', 'camion_asignado', 'pregunta_1', 'respuesta_1',
            'pregunta_2', 'respuesta_2'
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


class RecuperacionForm(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        })
    )


class PreguntasSeguridadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        input_attrs = {
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Tu respuesta...'
        }
        
        self.fields['respuesta_1'] = forms.CharField(
            label=self.user.get_pregunta_1_display(),
            widget=forms.TextInput(attrs=input_attrs),
            required=True
        )
        
        self.fields['respuesta_2'] = forms.CharField(
            label=self.user.get_pregunta_2_display(),
            widget=forms.TextInput(attrs=input_attrs),
            required=True
        )
        
        password_attrs = {
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }
        
        self.fields['nueva_password'] = forms.CharField(
            label='Nueva Contraseña',
            widget=forms.PasswordInput(attrs={
                **password_attrs,
                'placeholder': 'Mínimo 8 caracteres'
            }),
            validators=[MinLengthValidator(8)],
            required=True
        )
        
        self.fields['confirmar_password'] = forms.CharField(
            label='Confirmar Nueva Contraseña',
            widget=forms.PasswordInput(attrs={
                **password_attrs,
                'placeholder': 'Repite tu nueva contraseña'
            }),
            required=True
        )

    def clean(self):
        cleaned_data = super().clean()
        respuesta_1 = cleaned_data.get('respuesta_1', '').strip().lower()
        respuesta_2 = cleaned_data.get('respuesta_2', '').strip().lower()
        nueva_password = cleaned_data.get('nueva_password')
        confirmar_password = cleaned_data.get('confirmar_password')
        
        if respuesta_1 != self.user.respuesta_1.lower():
            self.add_error('respuesta_1', 'La respuesta no es correcta')
            
        if respuesta_2 != self.user.respuesta_2.lower():
            self.add_error('respuesta_2', 'La respuesta no es correcta')
            
        if nueva_password and nueva_password != confirmar_password:
            self.add_error('confirmar_password', 'Las contraseñas no coinciden')
            
        return cleaned_data

class EmailForm(forms.Form):
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'tu@ejemplo.com'
        })
    )