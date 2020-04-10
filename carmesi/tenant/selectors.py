

# Django
from django.db import models

# Third Parts
from tenant_schemas.utils import schema_context


class ClientQuerySet(models.query.QuerySet):

    def es_cliente(self, email):
        with schema_context('public'):
            return self.filter(email=email).exists()

    def listado_clientes(self):
        with schema_context('public'):
            return self.all().order_by('id')



class ClientManagers(models.Manager):

    def get_queryset(self):
        return ClientQuerySet(self.model, using=self._db)

    def es_cliente(self, email):
        return self.get_queryset().es_cliente(email)

    def listado_clientes(self):
        return self.get_queryset().listado_clientes()
