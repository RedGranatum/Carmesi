"""User model """

# standar library

# third.party

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# Utilities

# Models Serializers
from users.selectors import UserManagers

class User(AbstractUser):
    """User model.
    Extiende de Django Abstract User, y se cambio el username
    por email como campo principal
    """

    email = models.EmailField(
        'email adress',
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con ese email'
        }
    )

    is_client = models.BooleanField(
        'client status',
        default= True,
        help_text=('Si es un cliente del sistema')
        )

    is_verified = models.BooleanField(
        'verificado',
        default=False,
        help_text='Si el usuario ya verifico que es su correo'
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name','last_name']


    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username"""
        return self.username

    objects = UserManagers()
