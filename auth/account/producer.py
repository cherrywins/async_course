from confluent_kafka import Producer
import json
import uuid
import time
from jsonschema import validate
from .schemes import account_stream_schema_v2

def produce_message(topic_name, message):
    p = Producer({'bootstrap.servers': 'localhost:9094'})
    p.produce(topic_name, json.dumps(message))
    p.flush()

def produce_create_event(account):
    event = {
            'metadata': {
                'version': 2,
                'event_name': 'AccountCreated',
                'event_uuid': uuid.uuid4(),
                'timestamp': time.time()
            },
            'data': {
                'account_id': str(account.uuid),
                'email': account.email,
                'name': account.name,
                'role': account.role,
            }
        }
    validate(event, account_stream_schema_v2)
    produce_message('accounts-stream', event)

def produce_update_event(account):
    event = {
            'metadata': {
                'version': 2,
                'event_name': 'AccountUpdated',
                'event_uuid': uuid.uuid4(),
                'timestamp': time.time()
            },
            'data': {
                'account_id': str(account.uuid),
                'email': account.email,
                'name': account.name,
                'role': account.role,
            }
        }
    validate(event, account_stream_schema_v2)
    produce_message('accounts-stream', event)
