from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Sum
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

class ClienteListView(ListView):
    model = Cliente
    template_name = "clientes/lista_clientes.html"
    context_object_name = "clientes"
    queryset = Cliente.objects.filter(activo=True)  # Solo clientes activos

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

class ClienteDetailView (DetailView):
    """Vista detallada de cliente con historial de despachos"""
    model = Cliente
    template_name = "clientes/detalle_cliente.html"
    context_object_name = "cliente"

def marcar_entregado(request, pk):
    """Función para cambiar estado de despacho a entregado"""
    despacho = get_object_or_404(Despacho, pk=pk)
    if not despacho.entregado:
        despacho.entregado = True
        despacho.cliente.debe_total -= despacho.cantidad_botellones
        despacho.cliente.save()
        despacho.save()
    return redirect('detalle_cliente', pk=despacho.cliente.pk)

class DespachoCreateView(CreateView):
    model = Despacho
    fields = ["cliente", "cantidad_botellones", "notas"]
    template_name = "clientes/nuevo_despacho.html"
    success_url = reverse_lazy("lista_clientes")

    def form_valid(self, form):
        """Actualiza la deuda automáticamente al crear despacho"""
        response = super().form_valid(form)
        self.object.cliente.debe_total += self.object.cantidad_botellones
        self.object.cliente.save()
        return response