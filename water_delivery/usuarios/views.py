from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserCreationForm, RecuperacionForm, PreguntasSeguridadForm, EmailForm  # Añade EmailForm
from .models import Usuario
from django.core.mail import send_mail
import secrets  # Para generar tokens seguros

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    
    def get_success_url(self):
        # Verifica si hay un parámetro 'next' en la URL
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
            
        # Redirige según el tipo de usuario
        if self.request.user.tipo_usuario == Usuario.EMPRESA:
            return reverse_lazy('clientes:dashboard')
        else:
            return reverse_lazy('clientes:lista_clientes')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('usuarios:login')


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'usuarios/register.html'
    success_url = reverse_lazy('usuarios:login')


class RecuperacionView(FormView):
    template_name = 'usuarios/recuperacion.html'
    form_class = RecuperacionForm
    success_url = reverse_lazy('usuarios:preguntas_seguridad')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        try:
            usuario = Usuario.objects.get(username=username)
            self.request.session['usuario_recuperacion'] = usuario.id
            return super().form_valid(form)
        except Usuario.DoesNotExist:
            messages.error(self.request, 'El usuario no existe. Por favor, ingrese un nombre de usuario válido.')
            return self.form_invalid(form)


class PreguntasSeguridadView(FormView):
    template_name = 'usuarios/preguntas_seguridad.html'
    form_class = PreguntasSeguridadForm
    success_url = reverse_lazy('usuarios:login')

    def dispatch(self, request, *args, **kwargs):
        if 'usuario_recuperacion' not in request.session:
            messages.error(request, 'Debe iniciar el proceso de recuperación primero')
            return redirect('usuarios:recuperar')
            
        self.usuario = get_object_or_404(Usuario, pk=request.session['usuario_recuperacion'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.usuario
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.usuario
        return kwargs

    def form_valid(self, form):
        nueva_password = form.cleaned_data['nueva_password']
        self.usuario.set_password(nueva_password)
        self.usuario.save()
        
        del self.request.session['usuario_recuperacion']
        messages.success(self.request, '¡Contraseña actualizada correctamente! Ahora puede iniciar sesión.')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class RestablecerContrasenaView(PreguntasSeguridadView):
    template_name = 'usuarios/restablecer_contrasena.html'
    
class RecuperacionEmailView(FormView):
    template_name = 'usuarios/recuperacion_email.html'
    form_class = EmailForm  # Necesitarás crear este formulario
    success_url = reverse_lazy('usuarios:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            usuario = Usuario.objects.get(email=email)
            
            # Generar token seguro
            token = secrets.token_urlsafe(32)
            usuario.token_recuperacion = token
            usuario.save()
            
            # Construir enlace de recuperación
            reset_url = self.request.build_absolute_uri(
                reverse('usuarios:resetear_con_token', kwargs={'token': token})
            )
            
            # Enviar email
            send_mail(
                'Recuperación de contraseña - Water Delivery',
                f'''Hola {usuario.username},
                
Para restablecer tu contraseña, por favor haz clic en el siguiente enlace:
{reset_url}

Si no solicitaste este cambio, ignora este mensaje.

Atentamente,
El equipo de Water Delivery''',
                DEFAULT_FROM_EMAIL,  # Usa la configuración de settings.py
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
    form_class = PreguntasSeguridadForm  # Reutilizamos el mismo formulario
    success_url = reverse_lazy('usuarios:login')

    def dispatch(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            self.usuario = Usuario.objects.get(token_recuperacion=token)
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
        self.usuario.token_recuperacion = None  # Invalidar el token después de usarlo
        self.usuario.save()
        
        messages.success(self.request, '¡Contraseña actualizada correctamente! Ahora puede iniciar sesión.')
        return super().form_valid(form)