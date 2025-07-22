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
    
    # Para mostrar el texto completo de las preguntas en lugar del código
    @admin.display(description='Pregunta 1')
    def get_pregunta_1_display(self, obj):
        return obj.get_pregunta_1_display()
    
    @admin.display(description='Pregunta 2')
    def get_pregunta_2_display(self, obj):
        return obj.get_pregunta_2_display()

admin.site.register(Usuario, UsuarioAdmin)