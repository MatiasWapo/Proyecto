# usuarios/urls.py
from django.urls import path
from .views import CustomLoginView, CustomRegisterView, CustomLogoutView
from django.contrib.auth.views import LogoutView

app_name = 'usuarios'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
]