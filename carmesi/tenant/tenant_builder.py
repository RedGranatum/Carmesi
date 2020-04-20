# DJANGO
from django.core.exceptions import ValidationError
from django.utils.text import slugify

# Utilities

# Third Parts
from tenant_schemas.utils import schema_exists, schema_context


# Models
from tenant.models import Client
from users.models import User


class TenantValidator(object):
    def validar_email_cliente(email):
        if Client.objects.es_cliente(email):
            raise ValidationError("Ya se existe un espacio registrado para ese email")

    def validar_nombre_cliente(schema_name):
        if schema_exists(schema_name):
            raise ValidationError("El nombre del cliente ya esta en uso, digita otro nombre")


class TenantBuilder(object):

    def __init__(self, email, owner_name, client_name,domain_url, password):
        self.email = email
        self.owner_name = owner_name
        self.client_name = client_name
        self.domain_url = domain_url
        self.usuario_principal = None
        self.password = password

    def get_schema_name(self):
        slug_client_name = slugify(self.client_name).replace("-", "")
        return slug_client_name

    def get_domain_name(self):
        return "{}.{}".format(self.get_schema_name(), self.domain_url)

    def validar_nombre_cliente(self):
        schema_name = self.get_schema_name()
        TenantValidator.validar_nombre_cliente(schema_name)

    def validar_email_cliente(self):
        TenantValidator.validar_email_cliente(self.email)

    def validar(self):
        self.validar_nombre_cliente()
        self.validar_email_cliente()

    def crear_usuario_principal(self):
        with schema_context(self.get_schema_name()):
            user = User(username=self.email, email=self.email, first_name=self.owner_name, last_name='')
            user.set_password(self.password)
            user.full_clean()
            user.save()
            self.usuario_principal = user

    def get_numero_usuarios(self):
        with schema_context(self.get_schema_name()):
            return User.objects.all().count()

    def crear(self):
        self.validar()
        client = Client()
        client.schema_name = self.get_schema_name()
        client.domain_url = self.get_domain_name()
        client.email = self.email
        client.owner_name = self.owner_name
        client.name = self.client_name

        client.save()

        self.crear_usuario_principal()
        return client
