from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserCreationForm, RecuperacionForm, PreguntasSeguridadForm, EmailForm
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
    form_class = PreguntasSeguridadForm
    success_url = reverse_lazy('usuarios:login')

    def dispatch(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            self.usuario = Usuario.objects.get(
                token_recuperacion=token,
                token_recuperacion_fecha__gte=timezone.now()-timedelta(hours=24)
            )
            return super().dispatch(request, *args, **kwargs)
        except Usuario.DoesNotExist:
            messages.error(request, 'El enlace de recuperación no es válido o ha expirado.')
            return redirect('usuarios:recuperar')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.usuario
        return kwargs

    def form_valid(self, form):
        nueva_password = form.cleaned_data['nueva_password']
        self.usuario.set_password(nueva_password)
        self.usuario.token_recuperacion = None
        self.usuario.token_recuperacion_fecha = None
        self.usuario.save()
        
        messages.success(self.request, '¡Contraseña actualizada correctamente! Ahora puede iniciar sesión.')
        return super().form_valid(form)