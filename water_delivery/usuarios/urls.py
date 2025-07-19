from django.urls import path
from .views import (
    CustomLoginView, 
    CustomLogoutView, 
    CustomRegisterView,
    RecuperacionEmailView,
    ResetearConTokenView,
)
app_name = 'usuarios'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('recuperar/', RecuperacionEmailView.as_view(), name='recuperar'),
    path('resetear/<str:token>/', ResetearConTokenView.as_view(), name='resetear_con_token'),
]