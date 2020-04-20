
# DJANGO

from tenant.models import Client

# Utilities

# Services & Builders

from nucleo.services.token import token_verification_email_new_client
from nucleo.services.token_builders import TokenFactory


from tenant.tenant_builder import TenantBuilder, TenantValidator

tokenFactory = TokenFactory()


def cliente_validar_email(email):
    TenantValidator.validar_email_cliente(email)


def cliente_validar_nombre(schema_name):
    TenantValidator.validar_nombre_cliente(schema_name)


def cliente_crear(
    *,
    token: str,
    client_name: str,
    password: str,
    domain_url: str,
      ) -> Client:

        cliente_validar_nombre(client_name)

        payload = token_verification_email_new_client(token)

        tenant = TenantBuilder(email=payload['email'],
                               owner_name=payload['owner_name'],
                               client_name=client_name,
                               domain_url=domain_url,
                               password=password)
        cliente = tenant.crear()
        return cliente

