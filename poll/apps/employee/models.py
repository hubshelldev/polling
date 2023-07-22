from __future__ import unicode_literals
from email.policy import default
from pyexpat import model
# from turtle import Turtle
# from types import CoroutineType

from django.contrib.auth import models as auth_models
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from apps.employee import managers

# from apps.phygital_generic import models as generic_models
# from apps.phygital_generic import tasks



class User(auth_models.AbstractBaseUser):
    """Custom user model that supports using email instead of username"""

    firstname = models.CharField(max_length=64)

    lastname = models.CharField(max_length=64)

    email = models.EmailField(max_length=64,blank=True,unique=True,null=True)

    phone_number = models.CharField(max_length=100, blank=True, null=True)

    roles = models.ForeignKey('RoleMaster', blank=True, null=True, on_delete=models.CASCADE)

    image = models.CharField(max_length=255, null=True,blank=True)

    is_block = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True)

    is_email_verified = models.BooleanField(default=False)

    is_phone_verified = models.BooleanField(default=False)

    pincode = models.IntegerField(null =True,blank=True)

    is_social = models.BooleanField(default=False)

    social_id = models.CharField(max_length=200,null=True)

    language = models.CharField(max_length=50,null=True)

    secretkey = models.CharField(max_length=20,null=True)

    created_on = models.DateTimeField(auto_now_add=True,null=True)

    blocked_reason = models.CharField(max_length=50,null=True)

    employee_id = models.CharField(max_length=20,null=True)

    designation = models.CharField(max_length=20,null=True)

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'

    @property
    def get_roles(self):
        if self.roles:
            return self.roles.name

    @property
    def is_admin(self):
        return self.get_roles and self.get_roles in ["SuperAdmin", "Employee"]

    @classmethod
    def create_user(cls, email):
        if email and not User.objects.filter(email=email).exists():
            role, _ = RoleMaster.objects.get_or_create(name='User')
            User.objects.create_user(email=email, roles=role)

class OTPAuth(models.Model):
    "Model for handling user authentication via OTP"

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    otp = models.CharField(max_length=12)
    expired_by = models.DateTimeField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        verbose_name = _('OTP Auth')
        verbose_name_plural = _('OTP Auth')



class RoleMaster(models.Model):
    "Model for handling user role"
    
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Role master')
        verbose_name_plural = _('Role masters')
