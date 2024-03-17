from billing.task.models import Task
from billing.account.models import Account, OperationLog
import logging
from datetime import datetime
log = logging.getLogger('reward')

def reward_assignee(task, assignee):
    assignee.balance = assignee.balance + task.reward
    assignee.save()
    OperationLog.objects.create(
      account=assignee,
      operation_type='reward',
      amount=task.reward,
      date=datetime.now(),
      task=task,
    )
    log.info(f'{str(assignee.uuid)} was rewarded with {task.cost}')
