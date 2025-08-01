"""
URL configuration for water_delivery project.

La lista urlpatterns enruta URLs a vistas. Incluye rutas para admin, usuarios y clientes.
La raíz redirige al login.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Función para redirigir la raíz al login (vista home)
def redirect_to_login(request):
    return redirect('usuarios:login')

# Rutas principales: admin, usuarios, clientes
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirigir la raíz del sitio al login
    path('', redirect_to_login, name='home'),
    
    # Apps
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('clientes/', include('clientes.urls', namespace='clientes')),
]
