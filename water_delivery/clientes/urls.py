from django.urls import path
from .views import *

app_name = 'clientes'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('lista/', ClienteListView.as_view(), name='lista_clientes'), # Nueva ruta
    path('nuevo/', ClienteCreateView.as_view(), name='nuevo_cliente'),
    path('<int:pk>/', ClienteDetailView.as_view(), name='detalle_cliente'),
    path('editar/<int:pk>/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('despacho/nuevo/', DespachoCreateView.as_view(), name='nuevo_despacho'),
    path('despacho/<int:pk>/entregado/', marcar_entregado, name='marcar_entregado'),
]