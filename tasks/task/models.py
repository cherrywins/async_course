from django.db import models
import uuid

class Task(models.Model):
    description = models.CharField(max_length=1024)
    status = models.CharField(max_length=255, null=True, blank=True, default='assigned')
    assignee = models.ForeignKey('account.Account', on_delete=models.SET_NULL, related_name='assignee', null=True)
