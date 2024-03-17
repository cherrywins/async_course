from django.db import models
import uuid

class Task(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    jira_id = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=1024)
    uuid = models.UUIDField(null=True, editable=False, unique=True)
    status = models.CharField(max_length=255, null=True, blank=True, default='assigned')
    assignee = models.ForeignKey('account.Account', on_delete=models.SET_NULL, related_name='assignee', null=True)
