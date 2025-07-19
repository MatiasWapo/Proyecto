from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserCreationForm, RecuperacionForm, PreguntasSeguridadForm, EmailForm, ResetPasswordForm
from .models import Usuario
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import secrets
from django.conf import settings


DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('clientes:lista_clientes')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('usuarios:login')

class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'usuarios/register.html'
    success_url = reverse_lazy('usuarios:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"Error en {form.fields[field].label}: {error}"
                )
        return super().form_invalid(form)

class RecuperacionEmailView(FormView):
    template_name = 'usuarios/recuperacion_email.html'
    form_class = EmailForm
    success_url = reverse_lazy('usuarios:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            usuario = Usuario.objects.get(email=email)
            
            token = secrets.token_urlsafe(32)
            usuario.token_recuperacion = token
            usuario.token_recuperacion_fecha = timezone.now()
            usuario.save()
            
            # Asegúrate que estás usando el nombre correcto de la URL
            reset_url = self.request.build_absolute_uri(
                reverse('usuarios:resetear_con_token', kwargs={'token': token})
            )
            
            send_mail(
                'Recuperación de contraseña - Water Delivery',
                f'''Hola {usuario.username},
                
Para restablecer tu contraseña, por favor haz clic en el siguiente enlace:
{reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, ignora este mensaje.

Atentamente,
El equipo de Water Delivery''',
                DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )
            
            messages.success(self.request, 'Se ha enviado un enlace de recuperación a tu correo electrónico.')
            return super().form_valid(form)
            
        except Usuario.DoesNotExist:
            messages.error(self.request, 'No existe una cuenta asociada a este correo electrónico.')
            return self.form_invalid(form)

class ResetearConTokenView(FormView):
    template_name = 'usuarios/resetear_con_token.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('usuarios:login')

    def dispatch(self, request, *args, **kwargs):
        token = kwargs.get('token')
        print(f"Token recibido: {token}")  # Debug
        
        try:
            self.usuario = Usuario.objects.get(
                token_recuperacion=token,
                token_recuperacion_fecha__gte=timezone.now()-timedelta(hours=24)
            )
            print(f"Usuario encontrado: {self.usuario.username}")  # Debug
            return super().dispatch(request, *args, **kwargs)
            
        except Usuario.DoesNotExist:
            print("Token inválido o expirado")  # Debug
            messages.error(request, 'El enlace de recuperación no es válido o ha expirado.')
            return redirect('usuarios:recuperar')

    def form_valid(self, form):
        print("Formulario válido, procesando...")  # Debug
        nueva_password = form.cleaned_data['nueva_password']
        
        # Validación adicional
        if nueva_password != form.cleaned_data['confirmar_password']:
            messages.error(self.request, 'Las contraseñas no coinciden')
            return self.form_invalid(form)
            
        self.usuario.set_password(nueva_password)
        self.usuario.token_recuperacion = None
        self.usuario.token_recuperacion_fecha = None
        self.usuario.save()
        
        print("Contraseña actualizada correctamente")  # Debug
        messages.success(self.request, '¡Contraseña actualizada correctamente! Ahora puede iniciar sesión.')
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Formulario inválido, errores:", form.errors)  # Debug
        return super().form_invalid(form)