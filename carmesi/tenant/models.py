from django.db import models
from tenant_schemas.models import TenantMixin

# Managers
from tenant.selectors import ClientManagers

# Create your models here.
class Client(TenantMixin):
    name = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    create_on = models.DateField(auto_now_add=True)
    email = models.EmailField(default='')
    owner_name = models.CharField(max_length=100)
    auto_create_schema =True
    auto_drop_schema = True # Nos permite borrar todo el esquema con delete

    objects = ClientManagers()
