from django.urls import path
from .views import *  # Importa todas las vistas excepto buscar_cliente_vista

app_name = 'clientes'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('lista/', ClienteListView.as_view(), name='lista_clientes'),
    path('nuevo/', ClienteCreateView.as_view(), name='nuevo_cliente'),
    path('<int:pk>/', ClienteDetailView.as_view(), name='detalle_cliente'),
    path('editar/<int:pk>/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('despacho/nuevo/', DespachoCreateView.as_view(), name='nuevo_despacho'),
    path('despacho/<int:pk>/entregado/', marcar_entregado, name='marcar_entregado'),
    
    # URLs del dashboard (mantenerlas)
    path('dashboard-despachos/', dashboard_despachos, name='dashboard_despachos'),
    path('api/clientes/', api_clientes_activos, name='api_clientes'),
    path('api/despachos-hoy/', api_despachos_hoy, name='api_despachos_hoy'),
    path('api/crear-despacho/', api_crear_despacho, name='api_crear_despacho'),
    path('api/crear-cliente/', api_crear_cliente, name='api_crear_cliente'),
    path('api/eliminar-despacho/<int:despacho_id>/', api_eliminar_despacho, name='api_eliminar_despacho'),
    path('api/marcar-entregado/<int:despacho_id>/', api_marcar_entregado, name='api_marcar_entregado'),
]