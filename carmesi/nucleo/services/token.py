# DJANGO
from django.conf import settings
from django.utils import timezone

# Utilities
import jwt
from datetime import timedelta

def token_verification(email, owner_name):
    """ Crea JWT token de validacion de cuenta"""

    exp_date = timezone.now() + timedelta(days=1)
    payload ={
        'user': email,
        'owner_name': owner_name,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation_new_client'
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()



def token_verification_email_new_client(token):
    """ Verify token new client is valid """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
    except jwt.ExpiredSignatureError:
        raise ValidationError("El token de verificacion ha expirado")
    except jwt.PyJWTError:
        raise ValidationError("El token no es valido")
    if payload['type'] != 'email_confirmation_new_client':
        raise ValidationError("El token no es valido para el registro")

    return payload
