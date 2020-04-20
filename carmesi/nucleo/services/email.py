
# DJANGO


# Utilities

# Services & Builders
from nucleo.services.email_builders import EmailBuilder
from tenant.services import cliente_validar_email
from users.services import usuario_validar_email

_email_builder = EmailBuilder()


def email_enviar_prealta_cliente(email, owner_name):
        cliente_validar_email(email)
        email = _email_builder.crear_de_tipo_cliente(email=email, name=owner_name)
        email.build_token()
        email.enviar()


def email_enviar_prealta_usuario(email, name):
        usuario_validar_email(email)
        email = _email_builder.crear_de_tipo_usuario(email=email, name=name)
        email.build_token()
        email.enviar()

