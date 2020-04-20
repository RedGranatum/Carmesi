# Django
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

# Third Parts
from tenant_schemas.utils import schema_exists

# Services & Builder
from tenant.tenant_builder import TenantBuilder


class ClienteTest(TestCase):

    def test_nuevo_cliente(self):

        tenant = TenantBuilder(email='nuevo_cliente@gmail.com',
                               owner_name='El nombre de la persona',
                               client_name='mi empresa',
                               domain_url='localhost',
                               password='1234')
        cliente = tenant.crear()

        self.assertTrue(schema_exists('miempresa'))
        self.assertEqual(cliente.email, 'nuevo_cliente@gmail.com')
        self.assertEqual(cliente.name, 'mi empresa')
        self.assertEqual(cliente.owner_name, 'El nombre de la persona')
        self.assertEqual(cliente.schema_name, 'miempresa')
        self.assertEqual(cliente.domain_url, 'miempresa.localhost')
        self.assertEqual(cliente.is_active, True)

        self.assertTrue(tenant.usuario_principal)
        self.assertEqual(tenant.get_numero_usuarios(), 1)
        self.assertEqual(tenant.usuario_principal.email, 'nuevo_cliente@gmail.com')
        self.assertEqual(tenant.usuario_principal.first_name,'El nombre de la persona')
        self.assertEqual(tenant.usuario_principal.last_name,'')
        self.assertTrue(check_password('1234', tenant.usuario_principal.password))

    def test_nuevo_cliente_con_espacios_en_client_name(self):

        tenant = TenantBuilder(email='nuevo_clienxte@gmail.com',
                               owner_name='El nombre de la persona',
                               client_name='mi   empresa nueva',
                               domain_url='localhost',
                               password='1234')
        schema_name = tenant.get_schema_name()
        self.assertEqual(schema_name, 'miempresanueva')

    def test_crea_cliente_con_nombre_que_ya_existe(self):
        tenant1 = TenantBuilder(email='nuevo_cliente@gmail.com',
                                owner_name='El nombre de la persona',
                                client_name='mi empresa',
                                domain_url='localhost',
                                password='1234')
        tenant1.crear()

        tenant2 = TenantBuilder(email='nuevo_correo@gmail.com',
                                owner_name='Nueva Persona',
                                client_name='mi empresa',
                                domain_url='localhost',
                                password='1234')

        with self.assertRaises(ValidationError) as cm:
            tenant2.crear()

        error = cm.exception

        self.assertEqual(error.message, 'El nombre del cliente ya esta en uso, digita otro nombre')

    def test_crea_cliente_con_un_email_que_ya_existe(self):
        tenant1 = TenantBuilder(email='nuevo_correo@gmail.com',
                                owner_name='El nombre de la persona',
                                client_name='empresa2',
                                domain_url='localhost',
                                password='1234')
        tenant1.crear()

        tenant2 = TenantBuilder(email='nuevo_correo@gmail.com',
                                owner_name='Nueva Persona',
                                client_name='empresa1',
                                domain_url='localhost',
                                password='1234')

        with self.assertRaises(ValidationError) as cm:
            tenant2.crear()

        error = cm.exception

        self.assertEqual(error.message, 'Ya se existe un espacio registrado para ese email')
