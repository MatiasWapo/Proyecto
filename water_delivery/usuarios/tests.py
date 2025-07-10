from django.test import TestCase
from django.urls import reverse
from .models import Usuario

class RecuperacionTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='testuser',
            password='testpass',
            respuesta_1='ciudad_real',
            respuesta_2='comida_real'
        )

    def test_recuperacion_flow(self):
        # Paso 1: Recuperación
        response = self.client.post(reverse('usuarios:recuperar'), {'username': 'testuser'})
        self.assertEqual(response.status_code, 302)  # Redirección
        
        # Paso 2: Preguntas
        session = self.client.session
        session['usuario_recuperacion'] = self.user.id
        session.save()
        
        response = self.client.post(reverse('usuarios:preguntas_seguridad'), {
            'respuesta_1': 'ciudad_real',
            'respuesta_2': 'comida_real',
            'nueva_password': 'NuevaPass123!',
            'confirmar_password': 'NuevaPass123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirección a login
        
    def test_respuestas_incorrectas(self):
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
        """Verifica que las respuestas estén hasheadas"""
        self.assertTrue(
            self.user.respuesta_1.startswith('pbkdf2_sha256$') or 
            self.user.respuesta_1.startswith('bcrypt$')
        )
        self.assertTrue(
            self.user.respuesta_2.startswith('pbkdf2_sha256$') or 
            self.user.respuesta_2.startswith('bcrypt$')
        )