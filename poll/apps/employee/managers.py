from __future__ import unicode_literals
import imp

from django.contrib.auth import models as auth_models
from django.utils.translation import gettext_lazy as _
from apps.employee import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        "Creates and saves a new user"

        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(email=self.normalize_email(email), **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        "Creates and saves a new superuser"
        
        user = self.create_user(email, password)
        has_value = models.RoleMaster.objects.filter().count()
        roles = ["SuperAdmin", "Employee"]
 
        if has_value ==0:
            for rol in roles:
                role=models.RoleMaster(name=rol)
                role.save()

        user.is_staff = True
        user.is_superuser = True
        user.roles_id=1
        user.save(using=self._db)
        return user