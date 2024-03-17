from django.db import models
import uuid 

class OperationLog(models.Model):
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='worker', null=True)
    operation_type = models.CharField(max_length=255, blank=True, null=True)
    amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE, related_name='task', null=True)
    date = models.DateTimeField(null=True, blank=True)
    is_processed = models.BooleanField(null=True, default=False)
    
    
class PayOutLog(models.Model):
    uuid = models.UUIDField(null=True, default=uuid.uuid4)
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='account', null=True)
    amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
