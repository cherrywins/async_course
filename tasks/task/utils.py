from task.models import Task
from account.models import Account
import random

from task.producer import produce_task_assign_event

def reassign_tasks():
    open_tasks = Task.objects.exclude(status='completed')
    assignee_ids = Account.objects.exclude(role__in=['manager', 'admin']).values_list('id', flat=True)
    for task in open_tasks:
        task.assignee_id = int(random.choice(assignee_ids))
        task.save()
        produce_task_assign_event(task)
        
        
