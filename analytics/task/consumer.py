from confluent_kafka import Consumer, KafkaException

from .models import Task
import json
from jsonschema import validate
from .schemes import tasks_stream_schema_v1, tasks_complete_schema_v1
import logging
from datetime import datetime

log = logging.getLogger("billing_task_consumer")
    
def process_stream_message_v1(message):
    if message["metadata"]["event_name"] == "TaskCreated":
        task = Task.objects.filter(uuid=message["data"]["task_id"]).first() # in case we got the update event with prices first
        if not task:
            task = Task.objects.create(
                uuid=message["data"]["task_id"]
            )
        task.status="assigned",
        task.date_created=message["data"]["date_created"]
        task.save()
    elif message["metadata"]["event_name"] == "TaskUpdated":
        task = Task.objects.filter(uuid=message["data"]["task_id"]).first()  # we got the 'created' event first
        if not task:
            task = Task.objects.create(
                uuid=message["data"]["task_id"]
            )
        task.cost = message["data"]["cost"]
        task.reward = message["data"]["reward"]
        task.save()
        
def process_complete_message_v1(message):
    if message["metadata"]["event_name"] == "TaskCompleted":
        task = Task.objects.filter(
            uuid=message["data"]["task_id"],
        ).first()
        task.status = "completed"
        task.date_completed = datetime.now().date()
        task.save()

def validate_and_process_tasks_stream_event(message):
    """
        Creation and update of tasks
    """
    print(f"Processing message: {message}")
    message = json.loads(message)
    try:
        validate(message, tasks_stream_schema_v1)
        process_stream_message_v1(message)
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
        "bootstrap.servers": "localhost:9094",
        "group.id": "analytics",
        "auto.offset.reset": "earliest"
    })

    consumer.subscribe([topic_name])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            break
        if msg.error():
            raise KafkaException(msg.error())
        if topic_name == "tasks-stream":
            validate_and_process_tasks_stream_event(msg.value().decode("utf-8"))
        elif topic_name == "tasks-complete":
            validate_and_process_tasks_complete_event(msg.value().decode("utf-8"))
    consumer.close()
