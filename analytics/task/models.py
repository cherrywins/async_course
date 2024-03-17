from django.db import models

class Task(models.Model):
    uuid = models.UUIDField(null=True, editable=False, unique=True)
    status = models.CharField(max_length=255, null=True, blank=True)  # assigned, completed
    cost = models.PositiveIntegerField(null=True, default=1)
    reward = models.PositiveIntegerField(null=True, default=1)
    date_created = models.DateField(null=True)
    date_completed = models.DateField(null=True)
