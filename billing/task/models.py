from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    jira_id = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=1024)
    uuid = models.UUIDField(null=True, editable=False, unique=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    assignee = models.ForeignKey('account.Account', on_delete=models.SET_NULL, related_name='assignee', null=True)
    cost = models.PositiveIntegerField(null=True, default=1)
    reward = models.PositiveIntegerField(null=True, default=1)
    
    
class DeadQueueTaskEvent(models.Model):
    uuid=models.UUIDField(null=True, editable=False, unique=True)
    name=models.CharField(max_length=1024, editable=False)
    timestamp=models.DateTimeField()
    task_id=models.UUIDField(null=True, editable=False, unique=True)
    assignee_id=models.UUIDField(null=True, editable=False, unique=True)
    data=models.JSONField()
    sync_at=models.DateTimeField(null=True, default=None, editable=False)
    atempts=models.PositiveIntegerField(null=True, default=0)
    
