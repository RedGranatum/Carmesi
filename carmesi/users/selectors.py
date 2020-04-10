

# Django
from django.db import models
from django.contrib.auth.models import BaseUserManager



class UserQuerySet(models.query.QuerySet):
    def get_list(self):
        return self.all()


class UserManagers(BaseUserManager):

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def get_list(self):
        return self.get_queryset()
