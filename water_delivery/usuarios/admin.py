# =============================================
# CONFIGURACIÓN DEL ADMINISTRADOR DE USUARIOS
# =============================================
# Este archivo registra el modelo de usuario personalizado en el panel de administración
# de Django y personaliza su visualización, filtros y campos adicionales.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    # Lista de campos a mostrar en la tabla principal
    list_display = ('username', 'email', 'tipo_usuario', 'is_active', 'is_superuser', 'camion_asignado')
    list_filter = ('tipo_usuario', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'tipo_usuario')
    ordering = ('-is_superuser', '-is_active', 'username')
    
    # Campos para la edición detallada
    fieldsets = UserAdmin.fieldsets + (
        ('Datos adicionales', {
            'fields': (
                'tipo_usuario',
                'telefono',
                'direccion',
                'camion_asignado',
            ),
        }),
    )
    
    # Campos de solo lectura (opcional)
    readonly_fields = ('get_pregunta_1_display', 'get_pregunta_2_display')
    
    # Métodos para mostrar el texto completo de las preguntas de seguridad
    @admin.display(description='Pregunta 1')
    def get_pregunta_1_display(self, obj):
        return obj.get_pregunta_1_display()
    
    @admin.display(description='Pregunta 2')
    def get_pregunta_2_display(self, obj):
        return obj.get_pregunta_2_display()

# Registro del modelo Usuario en el admin
admin.site.register(Usuario, UsuarioAdmin)