# =============================================
# TESTS AUTOMATIZADOS PARA LA APP DE USUARIOS
# =============================================
# Este archivo contiene pruebas unitarias para la recuperación de contraseña,
# validación de respuestas de seguridad y correcto hasheo de datos sensibles.

from django.test import TestCase
from django.urls import reverse
from .models import Usuario

class RecuperacionTests(TestCase):
    """
    Pruebas para el flujo de recuperación de contraseña y validación de respuestas.
    """
    def setUp(self):
        # Crea un usuario de prueba con respuestas de seguridad
        self.user = Usuario.objects.create_user(
            username='testuser',
            password='testpass',
            respuesta_1='ciudad_real',
            respuesta_2='comida_real'
        )

    def test_recuperacion_flow(self):
        """
        Prueba el flujo completo de recuperación: solicitud, preguntas y cambio de contraseña.
        """
        # Paso 1: Recuperación
        response = self.client.post(reverse('usuarios:recuperar'), {'username': 'testuser'})
        self.assertEqual(response.status_code, 302)  # Redirección
        
        # Paso 2: Preguntas
        session = self.client.session
        session['usuario_recuperacion'] = self.user.id
        session.save()
        
        response = self.client.post(reverse('usuarios:preguntas_seguridad'), {
            'respuesta_1': 'ciudad_real',
            'respuesta_2': 'comida_real',  # Ambas correctas
            'nueva_password': 'NuevaPass123!',
            'confirmar_password': 'NuevaPass123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirección a login
        
    def test_respuestas_incorrectas(self):
        """
        Prueba que el sistema detecta respuestas incorrectas y muestra error.
        """
        session = self.client.session
        session['usuario_recuperacion'] = self.user.id
        session.save()
        
        response = self.client.post(reverse('usuarios:preguntas_seguridad'), {
            'respuesta_1': 'respuesta_incorrecta',
            'respuesta_2': 'comida_real',  # Una correcta y otra no
            'nueva_password': 'NuevaPass123!',
            'confirmar_password': 'NuevaPass123!'
        })
        self.assertEqual(response.status_code, 200)  # No redirecciona
        self.assertContains(response, "Respuesta incorrecta")  # Verifica mensaje de error

    def test_hasheo_respuestas(self):
        """
        Verifica que las respuestas de seguridad estén hasheadas correctamente.
        """
        self.assertTrue(
            self.user.respuesta_1.startswith('pbkdf2_sha256$') or 
            self.user.respuesta_1.startswith('bcrypt$')
        )
        self.assertTrue(
            self.user.respuesta_2.startswith('pbkdf2_sha256$') or 
            self.user.respuesta_2.startswith('bcrypt$')
        )