# =============================================
# MIDDLEWARE DE AUTENTICACIÓN GLOBAL
# =============================================
# Este middleware fuerza que todas las páginas requieran login, excepto las rutas
# públicas (login, registro, recuperación, admin, etc). Si el usuario no está autenticado
# y la URL no es pública, lo redirige al login.

from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware personalizado que exige autenticación en todas las páginas,
    excepto en las rutas exentas definidas en 'exempt_paths'.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que NO requieren login (páginas públicas)
        exempt_paths = [
            '/usuarios/login/',
            '/usuarios/register/',
            '/usuarios/recuperar/',
            '/usuarios/resetear/',
            '/admin/',
        ]
        # Si el usuario no está autenticado y la URL no es pública, redirige al login
        if not request.user.is_authenticated:
            if not any(request.path.startswith(path) for path in exempt_paths):
                return redirect('usuarios:login')
        # Si está autenticado o la URL es pública, continúa normalmente
        response = self.get_response(request)
        return response
