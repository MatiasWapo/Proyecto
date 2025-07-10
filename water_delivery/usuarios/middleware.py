from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que NO requieren login (páginas públicas)
        exempt_paths = [
            '/usuarios/login/',
            '/usuarios/register/',
            '/usuarios/recuperar/',
            '/usuarios/preguntas-seguridad/',
            '/admin/',
        ]
        
        # Si el usuario no está autenticado
        if not request.user.is_authenticated:
            # Verificar si la URL actual está en las páginas públicas
            if not any(request.path.startswith(path) for path in exempt_paths):
                return redirect('usuarios:login')
        
        response = self.get_response(request)
        return response
