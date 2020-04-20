# DJANGO

# Utilities

# Services & Builders
from nucleo.services.token_builders import (
    TokenFactory
    )

tokenFactory = TokenFactory()



def token_crear_token_login(email, schema_name):
    data = {'email': email, 'schema_name': schema_name}

    token_login = tokenFactory.crear_token_usuario_login(data)
    return token_login.get_jwt()


def token_verification_email_new_client(token):
    token_cliente = tokenFactory.crear_token_cliente()
    payload = token_cliente.decodificar_token(token)
    return payload


def token_verification_email_new_user(token):

    token_usuario = tokenFactory.crear_token_usuario()
    payload = token_usuario.decodificar_token(token)
    return payload


def token_verification_login(token):

    token_usuario = tokenFactory.crear_token_usuario_login()
    payload = token_usuario.decodificar_token(token)
    return payload
