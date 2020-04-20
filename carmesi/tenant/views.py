# Django
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated


# Models Serializers
from tenant.models import Client

# Selectors

# Services
from tenant.services import(
    cliente_crear
)

from nucleo.services.email import email_enviar_prealta_cliente
from nucleo.services.token import token_verification_email_new_client


class RegistroListadoApi(APIView):
    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ('schema_name','email','owner_name')

    def get(self, request):
        clientes = Client.objects.listado_clientes()

        serializer = self.OutputSerializer(clientes, many=True)
        return Response(serializer.data)

class RegistroApi(APIView):

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        owner_name = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_enviar_prealta_cliente(**serializer.validated_data)
        return Response(serializer.data,status=status.HTTP_200_OK)


class RegistroVericarNuevoClienteApi(APIView):

    class InputSerializer(serializers.Serializer):
        token = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = token_verification_email_new_client(**serializer.validated_data)

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
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # para obtener el domain_url tambien se puede usar request.META['HTTP_HOST']
        serializer.validated_data['domain_url'] = request.tenant.domain_url

        client = cliente_crear(**serializer.validated_data)
        serializer_out = self.OutputSerializer(client)
        return Response(serializer_out.data, status=status.HTTP_200_OK)
