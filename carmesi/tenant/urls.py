# Django
from django.urls import  path

# Views
from tenant.views import (
    RegistroListadoApi,
    RegistroApi,
    RegistroVericarNuevoClienteApi,
    RegistroCrearNuevoClienteApi
)

urlpatterns =[
    path('api/registro/listado', RegistroListadoApi.as_view(), name='registro_listado'),
    path('api/registro/', RegistroApi.as_view(), name='registro'),
    path('api/registro/verificar_token_nuevo_cliente', RegistroVericarNuevoClienteApi.as_view(), name='vtoken_vnuevo_cliente'),
    path('api/registro/crear_nuevo_cliente', RegistroCrearNuevoClienteApi.as_view(), name='registro_crear_nuevo_cliente'),
]
