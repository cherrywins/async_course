from task.models import Task
from account.models import Account
import random

def reassign_tasks():
    open_tasks = Task.objects.exclude(status='closed')
    assignee_ids = Account.objects.values_list('id', flat=True)
    for task in open_tasks:
        task.assignee_id = int(random.choice(assignee_ids))
        task.save()
