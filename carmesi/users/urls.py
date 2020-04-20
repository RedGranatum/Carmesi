# Django
from django.urls import path

# Views
from users.views import (
     UserApi,
     UserRegisterApi,
     UserVerificarTokenApi,
     UserLoginApi,
     UserLoginVerificarTokenApi,
     )

urlpatterns =[
    path('api/usuarios/', UserApi.as_view(), name='user_crud'),
    path('api/usuarios/registro/', UserRegisterApi.as_view(), name='user_register'),
    path('api/usuarios/verificar_token_nuevo_usuario/', UserVerificarTokenApi.as_view(), name='token_vnuevo_usuario'),

    path('api/usuarios/login/', UserLoginApi.as_view(), name='login'),
    path('api/usuarios/verificar_token_login/', UserLoginVerificarTokenApi.as_view(), name='token_vlogin_usuario'),

]
