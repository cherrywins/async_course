from django.db import models

# your_app_name/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Account(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    USERNAME_FIELD = 'uuid'
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="account_user_set", 
        related_query_name="account_user_group",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name="account_user_permissions", 
        related_query_name="account_user_permission",
    )

    def __str__(self):
        return self.name
