from confluent_kafka import Producer
import json
import uuid
import time
from datetime import datetime
from jsonschema import validate
from .schemes import tasks_stream_schema_v1, tasks_complete_schema_v1, tasks_assign_schema_v1

def produce_message(topic_name, message):
    p = Producer({'bootstrap.servers': 'localhost:9094'})
    p.produce(topic_name, json.dumps(message))
    p.flush()

def produce_task_create_event(task):
    event = {
        'metadata': {
            'version': 1,
            'event_name': 'TaskCreated',
            'event_uuid': uuid.uuid4(),
            'timestamp': time.time()
        },
        'data': {
            'task_id': str(task.uuid),
            'assignee_id': task.asignee.uuid,
            'title': task.title,
            'jira_id': task.jira_id,
            'date_created': datetime.now().date(),
        }
    }
    validate(event, tasks_stream_schema_v1)
    produce_message('tasks-stream', event)

    
    
def produce_task_complete_event(task):
    event = {
            'metadata': {
                'version': 1,
                'event_name': 'TaskCompleted',
                'event_uuid': uuid.uuid4(),
                'timestamp': time.time()
            },
            'data': {
                'task_id': str(task.uuid),
            }
        }
    validate(event, tasks_complete_schema_v1)
    produce_message('tasks-complete', event)
    

def produce_task_assign_event(task):
    event = {
            'metadata': {
                'version': 1,
                'event_name': 'TaskAssigned',
                'event_uuid': uuid.uuid4(),
                'timestamp': time.time()
            },
            'data': {
                'task_id': str(task.uuid),
                'assignee_id': task.assignee.uuid,
            }
        }
    validate(event, tasks_assign_schema_v1)
    produce_message('tasks-assign', event)
    
