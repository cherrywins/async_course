from django.db import models
import uuid

class PayOutLog(models.Model):
    uuid = models.UUIDField(null=True, default=uuid.uuid4)
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='account', null=True)
    amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
