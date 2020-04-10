from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

# Django
from rest_framework import  serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Models Serializers
from users.models import User

# Selectors
from users.services import user_create



class UserApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username','first_name','last_name')

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('email','first_name','last_name','password')

    def get(self, request):
        users = User.objects.get_list()
        serializer = self.OutputSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.InputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
