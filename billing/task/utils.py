import random
from billing.task.models import Task
from billing.task.producer import produce_task_update_event


def define_task_costs(task: Task):
    task.cost = random.randint(10, 20)
    task.reward = random.randint(20, 40)
    task.save()
    produce_task_update_event(task)
