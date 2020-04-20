# Django
from django.test import TestCase
from django.core import mail

# Services & Builder

from nucleo.services.email_builders import EmailBuilder


class EmailCreacionTest(TestCase):

    def test_email_prealta_cliente(self):
        data = {'email':'raultr@gmail.com', 'name':'Raul Enrique Torres Reyes','token': ''}

        email_builder = EmailBuilder()
        email = email_builder.crear_de_tipo_cliente(data['email'],data['name'])

        body = email.get_body()

        self.assertEqual(len(body), 4)
        self.assertEqual(body['email'], 'raultr@gmail.com')
        self.assertEqual(body['name'], 'Raul Enrique Torres Reyes')
        self.assertEqual(body['subject'], 'Hola Raul Enrique Torres Reyes Para continuar con tu registro en Carmesi, verifica tu email')

        msg_content = body['content']
        self.assertTrue(msg_content.startswith('<html>'))
        self.assertIn('<a href="">link</a>',msg_content)
        self.assertTrue(msg_content.endswith('</html>'))

    def test_email_prealta_usuario(self):
        data = {'email':'dianatr@gmail.com', 'name':'Diana Torres Reyes','token': ''}

        email_builder = EmailBuilder()
        email = email_builder.crear_de_tipo_usuario(data['email'],data['name'])

        body = email.get_body()

        self.assertEqual(len(body), 4)
        self.assertEqual(body['email'], 'dianatr@gmail.com')
        self.assertEqual(body['name'], 'Diana Torres Reyes')
        self.assertEqual(body['subject'], 'Hola Diana Torres Reyes Para continuar con tu registro en Carmesi como usuario de, verifica tu email.')

        msg_content = body['content']
        self.assertTrue(msg_content.startswith('<html>'))
        self.assertIn('<a href="">link</a>',msg_content)
        self.assertTrue(msg_content.endswith('</html>'))

    def test_enviar_email_prealta_usuario(self):
        data = {'email':'dianatr@gmail.com', 'name':'Diana Torres Reyes'}

        email_builder = EmailBuilder()
        email = email_builder.crear_de_tipo_usuario(data['email'],data['name'])
        email.enviar()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['dianatr@gmail.com'])
        self.assertEqual(mail.outbox[0].from_email, 'administrador@redgranatum.com')
        self.assertEqual(mail.outbox[0].subject, 'Hola Diana Torres Reyes Para continuar con tu registro en Carmesi como usuario de, verifica tu email.')
        self.assertTrue(mail.outbox[0].body.startswith('<html>'))

    def test_enviar_email_prealta_cliente(self):
        data = {'email':'raultr@gmail.com', 'name':'Raul Enrique Torres Reyes'}

        email_builder = EmailBuilder()
        email = email_builder.crear_de_tipo_cliente(data['email'],data['name'])
        email.enviar()

        self.assertEqual(len(mail.outbox), 1)
