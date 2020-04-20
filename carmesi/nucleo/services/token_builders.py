# DJANGO
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

# Utilities
from datetime import timedelta
import jwt


def fecha_expiracion():
    fecha = timezone.now() + timedelta(days=1)
    return int(fecha.timestamp())


TOKEN_TIPO_CLIENTE = 'email_confirmation_new_client'
TOKEN_TIPO_USUARIO = 'email_confirmation_new_user'
TOKEN_TIPO_USUARIO_LOGIN = 'user_login'


class TokenBase(object):

    def __init__(self, email=None, fun_fecha=fecha_expiracion):
        self.set_email(email)
        self.set_exp(fun_fecha())
        self.owner_name = None
        self.name = None
        self.type = None
        self.schema_name = None
        self.payload = {}

    def set_email(self, email):
        self.email = email

    def set_exp(self, exp):
        self.exp = exp

    def set_owner_name(self, owner_name):
        self.owner_name = owner_name

    def set_name(self, name):
        self.name = name

    def set_schema_name(self, schema_name):
        self.schema_name = schema_name

    def get_type(self):
        return ''

    def get_payload(self):
        self.payload['email'] = self.email
        self.payload['exp'] = self.exp
        self.payload['owner_name'] = self.owner_name
        self.payload['name'] = self.name
        self.payload['schema_name'] = self.schema_name
        self.payload['type'] = self.get_type()

        # Armamos el diccionario solo con los valores que no son None
        return {k: v for k, v in self.payload.items() if v is not None}

    def get_jwt(self):
        payload = self.get_payload()
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()

    def get_mensaje_validacion(self):
        return ''

    def decodificar_token(self, token):
        """ Verify token is valid """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
        except jwt.ExpiredSignatureError:
            raise ValidationError("El token de verificacion ha expirado")
        except jwt.PyJWTError:
            raise ValidationError("El token no es valido")
        if payload['type'] != self.get_type():
            mensaje = self.get_mensaje_validacion()
            raise ValidationError(mensaje)

        return payload


class TokenCliente(TokenBase):

    def __init__(self, email=None, owner_name=None,
                 fun_fecha=fecha_expiracion):
        super().__init__(email,fun_fecha)
        self.set_owner_name(owner_name)

    def get_type(self):
        return TOKEN_TIPO_CLIENTE

    def get_mensaje_validacion(self):
        return 'El token no es valido para el registro de cliente'


class TokenUsuario(TokenBase):
    def __init__():
        pass

    def __init__(self, email=None, name=None, schema_name=None, fun_fecha=fecha_expiracion):
        super().__init__(email,fun_fecha)
        self.set_name(name)
        self.set_schema_name(schema_name)

    def get_type(self):
        return TOKEN_TIPO_USUARIO

    def get_mensaje_validacion(self):
        return 'El token no es valido para el registro de usuario'


class TokenUsuarioLogin(TokenBase):

    def __init__(self, email=None, fun_fecha=fecha_expiracion, schema_name=None):
        super().__init__(email,fun_fecha)
        self.set_schema_name(schema_name)

    def get_type(self):
        return TOKEN_TIPO_USUARIO_LOGIN

    def get_mensaje_validacion(self):
        return 'El token no es valido para el ingreso al sistema'

class TokenFactory(object):

    def __init__(self, fun_fecha_exp=fecha_expiracion):
        self.fun_fecha = fun_fecha_exp

    def crear_token_cliente(self, data={}):
        return TokenCliente(**data, fun_fecha= self.fun_fecha)

    def crear_token_usuario(self, data={}):
        return TokenUsuario(**data, fun_fecha= self.fun_fecha)

    def crear_token_usuario_login(self, data={}):
        return TokenUsuarioLogin(**data, fun_fecha= self.fun_fecha)
