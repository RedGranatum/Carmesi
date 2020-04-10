from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _



# Django
from rest_framework import  serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Models Serializers
from users.models import User
from tenant.models import Client

# Selectors

# Services
from tenant.services import(
    client_create
)

from nucleo.services.email import(
    email_send_confirmation_preclient,
)
from nucleo.services.token import(
    token_verification_email_new_client,
)

class RegistroListadoApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ('schema_name','email','owner_name')
    def get(self, request):
        clientes = Client.objects.listado_clientes()

        #import ipdb;ipdb.set_trace()
        serializer = self.OutputSerializer(clientes, many=True)
        return Response(serializer.data)



class RegistroApi(APIView):

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        owner_name = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        # Revisamos que no exista un Tenant para ese email
        if Client.objects.es_cliente(serializer.data['email']):
            return Response({"Error":"Ya se existe un espacio registrado para ese email"},status=status.HTTP_403_FORBIDDEN)

        email_send_confirmation_preclient(serializer.data['email'],serializer.data['owner_name'])
        return Response(serializer.data,status=status.HTTP_200_OK)

class RegistroVericarNuevoClienteApi(APIView):

    class InputSerializer(serializers.Serializer):
        token = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        payload = token_verification_email_new_client(serializer.data['token'])

        return Response(payload, status=status.HTTP_200_OK)

class RegistroCrearNuevoClienteApi(APIView):

    class InputSerializer(serializers.Serializer):
        token = serializers.CharField(required=True)
        client_name = serializers.CharField(required=True,max_length=500)
        password = serializers.CharField(required=True, write_only=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ('schema_name','email','owner_name')

    def post(self, request):
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['domain_url'] = request.tenant.domain_url # O  #request.META['HTTP_HOST']
        client = client_create(**serializer.validated_data)
        serializer_out = self.OutputSerializer(client)
        return Response(serializer_out.data, status=status.HTTP_200_OK)
