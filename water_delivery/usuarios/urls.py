from django.urls import path
from .views import (
    CustomLoginView, 
    CustomLogoutView, 
    CustomRegisterView,
    RecuperacionView,
    PreguntasSeguridadView,
    RestablecerContrasenaView,
    RecuperacionEmailView,
    ResetearConTokenView,
)
app_name = 'usuarios'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('recuperar/', RecuperacionView.as_view(), name='recuperar'),
    path('preguntas-seguridad/', PreguntasSeguridadView.as_view(), name='preguntas_seguridad'),
    path('restablecer-contrasena/', RestablecerContrasenaView.as_view(), name='restablecer_contrasena'),
    path('recuperacion-email/', RecuperacionEmailView.as_view(), name='recuperacion_email'),
    path('resetear/<str:token>/', ResetearConTokenView.as_view(), name='resetear_con_token'),
]