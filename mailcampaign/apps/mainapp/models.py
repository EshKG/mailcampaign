from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm

from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime


class MailingList(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    template = models.CharField(max_length=100)
    status = models.CharField(max_length=30,
                              blank=True,
                              null=True)
    scheduled_time = models.DateTimeField(verbose_name=_("scheduled time"),
                                          blank=True,
                                          null=True)
    created_date = models.DateTimeField(default=timezone.now)
    finish_date = models.DateTimeField(blank=True,
                                        null=True)


class Subscribers(models.Model):
    """
    MAIL RECIPIENTS
    """
    email = models.EmailField(max_length=254,unique=True)
    first_name = models.CharField(max_length=100,
                                 blank=True,
                                 null=True)
    last_name = models.CharField(max_length=100,
                                 blank=True,
                                 null=True)
    birthday = models.DateField(blank=True,null=True)


class Message(models.Model):
    """
    STORES MESSAGE RECIPIENT, MESSAGE SUBJECT,
     MESSAGE STATUS
    """
    mailing = models.ForeignKey(to=MailingList, on_delete=models.CASCADE, related_name='messages')
    subscriber = models.ForeignKey(to=Subscribers, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    status = models.CharField(max_length=250,
                              blank=True,
                              null=True)
    read = models.BooleanField(verbose_name="Is message been read?",
                               default=False)



