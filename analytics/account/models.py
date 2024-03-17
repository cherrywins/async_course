import uuid

from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True, unique=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.UUIDField(null=False, default=uuid.uuid4, editable=False, unique=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.role} {self.name} {self.email}'
