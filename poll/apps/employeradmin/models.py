from django.db import models
from  apps.employee.models import *
from django.utils.translation import gettext_lazy as _
# Create your models here.

class EventMaster(models.Model):
    event_title = models.TextField(null=True)
    event_users = models.TextField(null=True)
    description = models.TextField(null=True)
    choices = models.JSONField(null=True)
    event_start = models.DateField(null=True)
    event_end = models.DateField(max_length=50,null=True)
    event_status = models.CharField(max_length=200,default="in progress",null=True)
    total_users = models.IntegerField(null=True)
    is_closed = models.BooleanField(default=False,null=True)
    is_delete = models.BooleanField(default=False,null=True)
    created_by = models.ForeignKey(User, related_name='event_admin_user', on_delete=models.CASCADE,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Event Master')
        verbose_name_plural = _('Event Master')

class EventChoiceMapping(models.Model):
    event = models.ForeignKey(EventMaster, related_name='eventchoice',on_delete=models.CASCADE,null=True)
    event_choice_name = models.TextField(null=True)
    event_choice_id = models.IntegerField(null=True)
    votes = models.IntegerField(null=True)

    class Meta:
        verbose_name = _('Event Choice Map')
        verbose_name_plural = _('Event Choice Map')

class EventUserMapping(models.Model):
    event = models.ForeignKey(EventMaster, related_name='eventuser',on_delete=models.CASCADE,null=True)
    event_user = models.ForeignKey(User, related_name='event_user_mapping', on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = _('Event User Map')
        verbose_name_plural = _('Event User Map')