# usuarios/views.py
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm  # Lo crearemos después

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True  # Si ya está logueado, redirige

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('usuarios:login')

class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'usuarios/register.html'
    success_url = reverse_lazy('usuarios:login')  # Redirige al login después de registrar