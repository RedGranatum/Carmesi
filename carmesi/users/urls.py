# Django
from django.urls import  path

# Views
from users.views import UserApi

urlpatterns =[
    path('api/usuarios/', UserApi.as_view(), name='user_crud'),

]
