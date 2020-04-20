# Django
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

# Models Serializers
from users.models import User

from nucleo.services.email import email_enviar_prealta_usuario
from nucleo.services.token import token_verification_email_new_user, token_verification_login

# Services
from users.services import usuario_listado,user_create_new, user_login


class UserApi(APIView):
    #permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        token = serializers.CharField(required=True)
        password = serializers.CharField(required=True, write_only=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username','first_name','last_name')

    def get(self, request):
        users = usuario_listado()
        serializer = self.OutputSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = user_create_new(**serializer.validated_data)

        serializer_out = self.OutputSerializer(user)
        return Response(serializer_out.data, status=status.HTTP_200_OK)


class UserRegisterApi(APIView):

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        name = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_enviar_prealta_usuario(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserVerificarTokenApi(APIView):

    class InputSerializer(serializers.Serializer):
        token = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)

        payload = token_verification_email_new_user(serializer.data['token'])

        return Response(payload, status=status.HTTP_200_OK)

class UserLoginApi(APIView):

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
        # Falta ponerle una longitud minima y maxima

    def post(self, request):

        serializer = self.InputSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)

        schema_name = request.tenant.schema_name
        data = user_login(**serializer.validated_data,schema_name=schema_name)

        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginVerificarTokenApi(APIView):

    class InputSerializer(serializers.Serializer):
        token = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = token_verification_login(**serializer.validated_data)

        return Response(payload, status=status.HTTP_200_OK)


