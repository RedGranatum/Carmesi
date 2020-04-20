
# Django
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


# Models Serializers
from users.models import User

from tenant_schemas.utils import schema_context

# Utilities
from operator import itemgetter

# Services
from nucleo.services.token import token_verification_email_new_user, token_verification_email_new_user, token_crear_token_login


def usuario_listado():
    return User.objects.get_list()


def usuario_validar_email(email):
    if User.objects.es_usuario(email):
        raise ValidationError("Ya existe un usuario registrado con ese email")


def user_create(
    *,
    email: str,
    first_name: str,
    last_name: str,
    password: str
) -> User:
    user = User(username=email, email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.full_clean()
    user.save()

    return user

def user_create_new(
    *,
    token: str,
    password: str
) -> User:

    payload = token_verification_email_new_user(token)
    usuario_validar_email(payload['email'])

    return user_create(
        email=payload['email'],
        first_name=payload['name'],
        last_name='',
        password=password
        )

def user_login(
    *,
    email: str,
    password: str,
    schema_name: str,
    ):
        user = authenticate(username=email, password=password)
        if not user:
            raise ValidationError("Error en el usuario o la contraseña")

        data = {'email':email,'schema_name': schema_name}
        token = token_crear_token_login(**data)

        return {'email': user.email, 'nombre': user.first_name, 'token': token}
