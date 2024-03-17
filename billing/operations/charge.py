from billing.task.models import Task
from billing.account.models import Account, OperationLog
import logging
from datetime import datetime
log = logging.getLogger('charge')

def charge_assignee(task: Task, assignee: Account):
    assignee.balance = assignee.balance - task.cost
    assignee.save()
    OperationLog.objects.create(
      account=assignee,
      operation_type='charge',
      amount=task.reward,
      date=datetime.now(),
      task=task,
    )
    log.info(f'{str(assignee.uuid)} was charged {task.cost}')
    