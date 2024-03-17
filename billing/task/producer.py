from confluent_kafka import Producer
import json
import uuid
import time
from datetime import datetime
from jsonschema import validate

from billing.task.models import Task
from .schemes import tasks_stream_schema_v1

def produce_message(topic_name, message):
    p = Producer({'bootstrap.servers': 'localhost:9094'})
    p.produce(topic_name, json.dumps(message))
    p.flush()

def produce_task_update_event(task: Task):
    event = {
            'metadata': {
                'version': 1,
                'event_name': 'TaskUpdated',
                'event_uuid': uuid.uuid4(),
                'timestamp': time.time()
            },
            'data': {
                'task_id': str(task.uuid),
                'cost': task.cost,
                'reward': task.reward,
            }
        }
    validate(event, tasks_stream_schema_v1)
    produce_message('tasks-stream', event)
    
