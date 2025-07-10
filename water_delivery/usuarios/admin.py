from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    # Lista de campos a mostrar en la tabla principal
    list_display = ('username', 'email', 'tipo_usuario', 'camion_asignado', 'get_pregunta_1_display', 'get_pregunta_2_display')
    
    # Campos para la edición detallada
    fieldsets = UserAdmin.fieldsets + (
        ('Datos adicionales', {
            'fields': (
                'tipo_usuario',
                'telefono',
                'direccion',
                'camion_asignado',
                'pregunta_1',  # Cambiado de pregunta_seguridad_1
                'respuesta_1',  # Cambiado de respuesta_seguridad_1
                'pregunta_2',  # Cambiado de pregunta_seguridad_2
                'respuesta_2'   # Cambiado de respuesta_seguridad_2
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