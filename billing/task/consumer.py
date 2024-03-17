from confluent_kafka import Consumer, KafkaException

from billing.operations.charge import charge_assignee
from billing.operations.reward import reward_assignee
from billing.task.utils import define_task_costs
from .models import Account, DeadQueueTaskEvent, Task
import json
from jsonschema import validate
from .schemes import tasks_stream_schema_v1, tasks_assign_schema_v1, tasks_complete_schema_v1, tasks_stream_schema_v2
import logging
from datetime import datetime

import random
log = logging.getLogger('billing_task_consumer')
    
def process_stream_message_v1(message):
    if message["metadata"]["event_name"] == "TaskCreated":
        task = Task.objects.create(
            uuid=message['data']['task_id'],
            asignee_id=message['data']['asignee_id'],
            title=message['data']['title'].split(']')[1],
            jira_id=['data']['title'].split(']')[0],
        )
        define_task_costs(task)
        
def process_stream_message_v2(message):
    if message["metadata"]["event_name"] == "TaskCreated":
        task = Task.objects.create(
            uuid=message['data']['task_id'],
            asignee_id=message['data']['asignee_id'],
            title=message['data']['title'],
            jira_id=['data']['jira_id'],
        )
        define_task_costs(task)

        
def process_assign_message_v1(message):
    if message["metadata"]["event_name"] == "TaskAssigned":
        task = Task.objects.filter(
            uuid=message['data']['task_id'],
        )
        if not task:
            log.error('The task has not been found')
            DeadQueueTaskEvent.objects.create(
                uuid=message["metadata"]["event_uuid"],
                name="TaskAssigned",
                timestamp=datetime.fromtimestamp(message["metadata"]["event_timestamp"]),
                task_uuid=message['data']['task_id'],
                assignee_uuid=message['data']['assignee_id'],
                data=message,
            )
            raise ValueError
        
        assignee = Account.objects.filter(uuid=message['data']['assignee_id'])
        if not assignee:
            log.error('The account has not been found')
            DeadQueueTaskEvent.objects.create(
                uuid=message["metadata"]["event_uuid"],
                name="TaskAssigned",
                timestamp=datetime.fromtimestamp(message["metadata"]["event_timestamp"]),
                task_uuid=message['data']['task_id'],
                assignee_uuid=message['data']['assignee_id'],
                data=message,
            )
            raise ValueError
        
        charge_assignee(task, assignee)


def process_complete_message_v1(message):
    if message["metadata"]["event_name"] == "TaskCompleted":
        task = Task.objects.filter(
            uuid=message['data']['task_id'],
        ).first()
        if not task:
            log.error('The task has not been found')
            DeadQueueTaskEvent.objects.create(
                uuid=message["metadata"]["event_uuid"],
                name="TaskCompleted",
                task_uuid=message['data']['task_id'],
                assignee_uuid=message['data']['assignee_id'],
                data=message,
            )
            return
    
        reward_assignee(task, task.assignee) 


def validate_and_process_tasks_stream_event(message):
    """
        Creation and update of tasks
    """
    print(f"Processing message: {message}")
    message = json.loads(message)
    try:
        if '[' in message['data']['title']:
            validate(message, tasks_stream_schema_v1)
            process_stream_message_v1(message)
        else:
            validate(message, tasks_stream_schema_v2)
            process_stream_message_v2(message)
    except Exception:
        log.error('Could not validate the scheme')
        

def validate_and_process_tasks_assign_event(message):
    """
        Task's assignation
    """
    log.info(f"Processing message: {message}")
    message = json.loads(message)
    try:
        validate(message, tasks_assign_schema_v1)
        process_assign_message_v1(message)
    except Exception:
        log.error('Could not validate the scheme')
        
        

def validate_and_process_tasks_complete_event(message):
    """
        Task's completion
    """
    log.info(f"Processing message: {message}")
    message = json.loads(message)
    try:
        validate(message, tasks_complete_schema_v1)
        process_complete_message_v1(message)
    except Exception:
        log.error('Could not validate the scheme')

def consume_messages(topic_name):
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9094',
        'group.id': 'billing',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([topic_name])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            break
        if msg.error():
            raise KafkaException(msg.error())
        if topic_name == 'tasks-stream':
            validate_and_process_tasks_stream_event(msg.value().decode('utf-8'))
        elif topic_name == 'tasks-assign':
            validate_and_process_tasks_assign_event(msg.value().decode('utf-8'))
        elif topic_name == 'tasks-complete':
            validate_and_process_tasks_complete_event(msg.value().decode('utf-8'))
    consumer.close()
