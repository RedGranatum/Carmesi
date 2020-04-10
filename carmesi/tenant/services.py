
# DJANGO
from django.core.exceptions import ValidationError

from tenant.models import Client
from tenant_schemas.utils import schema_context,tenant_context
from tenant_schemas.signals import post_schema_sync
from tenant_schemas.models import TenantMixin


# Utilities
import jwt
from datetime import timedelta
from operator import itemgetter

# Services
from users.services import user_create
from nucleo.services.token import token_verification_email_new_client

def client_create(
    *,
    token: str,
    client_name: str,
    password: str,
    domain_url: str,
    )-> Client:
        payload = token_verification_email_new_client(token)
        user, owner_name = itemgetter('user','owner_name')(payload)
        slug_name = client_name.replace(' ','').lower()

        if Client.objects.es_cliente(user):
            raise ValidationError("Ya se existe un espacio registrado para ese email")

        client = Client()
        client.schema_name = slug_name
        client.domain_url = "{}.{}".format(slug_name, domain_url)
        client.email =  user
        client.owner_name = owner_name
        client.name = owner_name

        client.password=password
        client.save()
        return client

# Se activa despues de guardar el client
def crear_usuario_admin_cliente(sender, tenant, **kwargs):
    """ After create Client create User """
    usuario = {'email':  tenant.email, 'first_name':tenant.owner_name,
        'last_name':'', 'password':tenant.password}
    with tenant_context(tenant):
        user_create(**usuario)

post_schema_sync.connect(crear_usuario_admin_cliente, sender=TenantMixin)
