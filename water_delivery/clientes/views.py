from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, datetime
import json
from .models import Cliente, Despacho

def dashboard(request):
    """Vista para el panel de control principal"""
    total_clientes = Cliente.objects.filter(activo=True).count()
    total_deuda = Cliente.objects.aggregate(Sum('debe_total'))['debe_total__sum'] or 0
    despachos_pendientes = Despacho.objects.filter(entregado=False).count()
    
    return render(request, 'clientes/dashboard.html', {
        'total_clientes': total_clientes,
        'total_deuda': total_deuda,
        'despachos_pendientes': despachos_pendientes,
    })

def dashboard_despachos(request):
    """Nueva vista para el dashboard de despachos diarios"""
    return render(request, 'clientes/despacho_nuevo.html')

# NUEVA FUNCIÓN - SOLO ESTA ES NUEVA
@login_required
def buscar_cliente_vista(request):
    """Vista para la página de búsqueda que redirige a buscar_cliente.html"""
    cliente = None
    
    if request.GET.get('buscar'):
        busqueda = request.GET.get('buscar').strip()
        
        # Buscar por nombre, apellido o teléfono
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellido__icontains=busqueda) |
            Q(telefono__icontains=busqueda),
            activo=True
        ).order_by('nombre')
        
        # Si hay resultados, redirigir a tu buscar_cliente.html existente
        if clientes.exists():
            cliente = clientes.first()
            # Redirigir a tu template buscar_cliente.html con el cliente encontrado
            return render(request, 'clientes/buscar_cliente.html', {'cliente': cliente})
    
    # Si no hay búsqueda o no se encontró nada, mostrar página de búsqueda
    return render(request, 'clientes/pagina_busqueda.html', {
        'cliente': cliente,
        'busqueda': request.GET.get('buscar', '')
    })

# APIs para el dashboard de despachos - NO TOCAR
def api_clientes_activos(request):
    """API para obtener lista de clientes activos"""
    clientes = Cliente.objects.filter(activo=True).values(
        'id', 'nombre', 'apellido', 'direccion', 'telefono'
    )
    
    clientes_list = []
    for cliente in clientes:
        clientes_list.append({
            'id': cliente['id'],
            'nombre': f"{cliente['nombre']} {cliente['apellido']}",
            'direccion': cliente['direccion'],
            'telefono': cliente['telefono']
        })
    
    return JsonResponse({'clientes': clientes_list})

def api_despachos_hoy(request):
    """API para obtener despachos del día actual"""
    hoy = date.today()
    despachos = Despacho.objects.filter(
        fecha__date=hoy
    ).select_related('cliente').order_by('-fecha')
    
    despachos_list = []
    for despacho in despachos:
        despachos_list.append({
            'id': despacho.id,
            'cliente': f"{despacho.cliente.nombre} {despacho.cliente.apellido}",
            'direccion': despacho.cliente.direccion,
            'cantidad': despacho.cantidad_botellones,
            'hora': despacho.fecha.strftime('%H:%M'),
            'notas': despacho.notas or '',
            'entregado': despacho.entregado
        })
    
    return JsonResponse({'despachos': despachos_list})

@csrf_exempt
@require_http_methods(["POST"])
def api_crear_despacho(request):
    """API para crear un nuevo despacho"""
    try:
        data = json.loads(request.body)
        cliente_id = data.get('cliente_id')
        cantidad = int(data.get('cantidad', 1))
        notas = data.get('notas', '')
        
        # Validar que el cliente existe
        cliente = get_object_or_404(Cliente, id=cliente_id, activo=True)
        
        # Crear el despacho
        despacho = Despacho.objects.create(
            cliente=cliente,
            cantidad_botellones=cantidad,
            notas=notas
        )
        
        # Actualizar la deuda del cliente MANUALMENTE
        cliente.debe_total += cantidad
        cliente.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Despacho creado exitosamente',
            'despacho': {
                'id': despacho.id,
                'cliente': f"{cliente.nombre} {cliente.apellido}",
                'cantidad': cantidad,
                'hora': despacho.fecha.strftime('%H:%M'),
                'notas': notas,
                'entregado': despacho.entregado
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al crear despacho: {str(e)}'
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_crear_cliente(request):
    """API para crear un nuevo cliente"""
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        apellido = data.get('apellido', '').strip()
        telefono = data.get('telefono', '').strip()
        direccion = data.get('direccion', '').strip()
        
        # Validaciones básicas
        if not nombre or not direccion:
            return JsonResponse({
                'success': False,
                'message': 'Nombre y dirección son requeridos'
            }, status=400)
        
        # Crear el cliente
        cliente = Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            direccion=direccion
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Cliente creado exitosamente',
            'cliente': {
                'id': cliente.id,
                'nombre': f"{cliente.nombre} {cliente.apellido}",
                'direccion': cliente.direccion,
                'telefono': cliente.telefono
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al crear cliente: {str(e)}'
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_eliminar_despacho(request, despacho_id):
    """API para eliminar un despacho"""
    try:
        despacho = get_object_or_404(Despacho, id=despacho_id)
        
        # Si el despacho no estaba entregado, restar de la deuda
        if not despacho.entregado:
            cliente = despacho.cliente
            cliente.debe_total -= despacho.cantidad_botellones
            cliente.save()
        
        despacho.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Despacho eliminado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al eliminar despacho: {str(e)}'
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_marcar_entregado(request, despacho_id):
    """API para marcar un despacho como entregado"""
    try:
        despacho = get_object_or_404(Despacho, id=despacho_id)
        
        if not despacho.entregado:
            despacho.entregado = True
            despacho.cliente.debe_total -= despacho.cantidad_botellones
            despacho.cliente.save()
            despacho.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Despacho marcado como entregado'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al marcar como entregado: {str(e)}'
        }, status=400)

# Mantén tus vistas existentes exactamente igual
class ClienteListView(ListView):
    model = Cliente
    template_name = "clientes/lista_clientes.html"
    context_object_name = "clientes"
    
    def get_queryset(self):
        queryset = Cliente.objects.filter(activo=True)
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(
                Q(nombre__icontains=buscar) |
                Q(apellido__icontains=buscar) |
                Q(telefono__icontains=buscar)
            )
        return queryset.order_by('nombre')

class ClienteCreateView(CreateView):
    model = Cliente
    fields = ["nombre", "apellido", "direccion", "telefono"]
    template_name = "clientes/nuevo_cliente.html"
    success_url = reverse_lazy('clientes:lista_clientes')

class ClienteUpdateView(UpdateView):
    model = Cliente
    fields = ["nombre", "apellido", "direccion", "telefono", "activo"]
    template_name = "clientes/editar_cliente.html"
    success_url = reverse_lazy("lista_clientes")

    def post(self, request, *args, **kwargs):
        if "activo" in request.POST:
            cliente = self.get_object()
            cliente.activo = False
            cliente.save()
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)

class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "clientes/detalle_cliente.html"
    context_object_name = "cliente"

def marcar_entregado(request, pk):
    despacho = get_object_or_404(Despacho, pk=pk)
    if not despacho.entregado:
        despacho.entregado = True
        despacho.cliente.debe_total -= despacho.cantidad_botellones
        despacho.cliente.save()
        despacho.save()
    return redirect('clientes:detalle_cliente', pk=despacho.cliente.pk)

class DespachoCreateView(CreateView):
    model = Despacho
    fields = ["cliente", "cantidad_botellones", "notas"]
    template_name = "clientes/nuevo_despacho.html"
    success_url = reverse_lazy("lista_clientes")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Actualizar la deuda manualmente
        self.object.cliente.debe_total += self.object.cantidad_botellones
        self.object.cliente.save()
        return response
