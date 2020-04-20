# Standar Library
from datetime import datetime, timezone

# Django
from django.test import TestCase
from django.core.exceptions import ValidationError

# Services & Builder

from nucleo.services.token_builders import(
    TokenFactory,
    TOKEN_TIPO_CLIENTE,
    TOKEN_TIPO_USUARIO,
    TOKEN_TIPO_USUARIO_LOGIN,
)

#Constantes
from .constant import (
    TOKEN_PREALTA_CLIENTE,
    TOKEN_PREALTA_CLIENTE_CADUCO,
    TOKEN_PREALTA_USUARIO,
    TOKEN_USUARIO_LOGIN,
)


def fecha_expiracion_2120():
    fecha = datetime(2120,1,1)
    epoch_timestamp = fecha.replace(tzinfo=timezone.utc).timestamp()
    return int(epoch_timestamp)


tokenFactory = TokenFactory(fun_fecha_exp=fecha_expiracion_2120)


class TokenBuilderTest(TestCase):

    def test_crear_payload_cliente(self):
        data = {'email':'raultr@gmail.com', 'owner_name':'Raul Enrique Torres Reyes'}
        token_cliente = tokenFactory.crear_token_cliente(data)
        payload = token_cliente.get_payload()
        self.assertEqual(len(payload), 4)
        self.assertEqual(payload['email'], 'raultr@gmail.com')
        self.assertEqual(payload['owner_name'], 'Raul Enrique Torres Reyes')
        self.assertEqual(payload['exp'], 4733510400)
        self.assertEqual(payload['type'], TOKEN_TIPO_CLIENTE)
        self.assertEqual(token_cliente.get_jwt(), TOKEN_PREALTA_CLIENTE)

    def test_crear_payload_usuario(self):
        data = {'email': 'raultr@gmail.com','name':'Raul Enrique Torres Reyes',
                'schema_name': 'mitiendita'}

        token_usuario = tokenFactory.crear_token_usuario(data)
        payload = token_usuario.get_payload()
        self.assertEqual(len(payload), 5)
        self.assertEqual(payload['email'], 'raultr@gmail.com')
        self.assertEqual(payload['name'], 'Raul Enrique Torres Reyes')
        self.assertEqual(payload['exp'], 4733510400)
        self.assertEqual(payload['type'], TOKEN_TIPO_USUARIO)
        self.assertEqual(payload['schema_name'], 'mitiendita')

        self.assertEqual(token_usuario.get_jwt(), TOKEN_PREALTA_USUARIO)

    def test_crear_payload_usuario_login(self):
        data = {'email':'raultr@gmail.com','schema_name': 'mitiendita'}

        token_login = tokenFactory.crear_token_usuario_login(data)
        payload = token_login.get_payload()
        self.assertEqual(len(payload), 4)
        self.assertEqual(payload['email'], 'raultr@gmail.com')
        self.assertEqual(payload['schema_name'], 'mitiendita')
        self.assertEqual(payload['exp'], 4733510400)
        self.assertEqual(payload['type'], TOKEN_TIPO_USUARIO_LOGIN)
        self.assertEqual(token_login.get_jwt(), TOKEN_USUARIO_LOGIN)

    def test_validar_token_prealta_cliente(self):
        token_cliente = tokenFactory.crear_token_cliente()

        data ={'email': 'raultr@gmail.com', 'owner_name': 'Raul Enrique Torres Reyes', 'exp': 4733510400, 'type': 'email_confirmation_new_client'}

        payload = token_cliente.decodificar_token(TOKEN_PREALTA_CLIENTE)
        self.assertDictEqual(payload, data)

    def test_validar_token_prealta_usuario(self):
        token_usuario = tokenFactory.crear_token_usuario()

        data ={'email': 'raultr@gmail.com', 'name': 'Raul Enrique Torres Reyes', 'exp': 4733510400, 'type': 'email_confirmation_new_user',
               'schema_name': 'mitiendita'}

        payload = token_usuario.decodificar_token(TOKEN_PREALTA_USUARIO)
        self.assertDictEqual(payload, data)

    def test_validar_token_prealta_usuario_login(self):
        token_usuario_login = tokenFactory.crear_token_usuario_login()

        data ={'email': 'raultr@gmail.com', 'exp': 4733510400, 'type': 'user_login',  'schema_name': 'mitiendita'}

        payload = token_usuario_login.decodificar_token(TOKEN_USUARIO_LOGIN)
        self.assertDictEqual(payload, data)

    def test_validar_mensaje_token_caduco(self):
        token_cliente = tokenFactory.crear_token_cliente()

        with self.assertRaises(ValidationError) as cm:
            token_cliente.decodificar_token(TOKEN_PREALTA_CLIENTE_CADUCO)

        error = cm.exception

        self.assertEqual(error.message, 'El token de verificacion ha expirado')

    def test_validar_mensaje_token_invalido(self):
        token_cliente = tokenFactory.crear_token_cliente()

        with self.assertRaises(ValidationError) as cm:
            token_invalido = TOKEN_PREALTA_CLIENTE[1:]
            token_cliente.decodificar_token(token_invalido)

        error = cm.exception
        self.assertEqual(error.message, 'El token no es valido')

    def test_validar_mensaje_token_tipo_cliente_difente(self):
        token_cliente = tokenFactory.crear_token_cliente()

        with self.assertRaises(ValidationError) as cm:
            token_cliente.decodificar_token(TOKEN_PREALTA_USUARIO)

        error = cm.exception
        self.assertEqual(error.message, 'El token no es valido para el registro de cliente')

    def test_validar_mensaje_token_tipo_usuario_difente(self):
        token_usuario = tokenFactory.crear_token_usuario()

        with self.assertRaises(ValidationError) as cm:
            token_usuario.decodificar_token(TOKEN_PREALTA_CLIENTE)

        error = cm.exception
        self.assertEqual(error.message, 'El token no es valido para el registro de usuario')

    def test_validar_mensaje_token_tipo_usuario__login_difente(self):
        token_usuario_login = tokenFactory.crear_token_usuario_login()

        with self.assertRaises(ValidationError) as cm:
            token_usuario_login.decodificar_token(TOKEN_PREALTA_USUARIO)

        error = cm.exception
        self.assertEqual(error.message, 'El token no es valido para el ingreso al sistema')
