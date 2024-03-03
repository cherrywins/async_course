from confluent_kafka import Producer
import json

def produce_message(topic_name, message):
    p = Producer({'bootstrap.servers': 'localhost:9094'})
    p.produce(topic_name, json.dumps(message))
    p.flush()

def produce_create_event(account):
    event = {
            'event_name': 'AccountCreated',
            'data': {
                'public_id': str(account.uuid),
                'email': account.email,
                'name': account.name,
                'role': account.role,
            }
        }
    produce_message('accounts-stream', event)

def produce_update_event(account):
    event = {
            'event_name': 'AccountUpdated',
            'data': {
                'public_id': str(account.uuid),
                'email': account.email,
                'name': account.name,
                'role': account.role,
            }
        }
    produce_message('accounts-stream', event)    

def produce_delete_event(uuid):
    event = {
            'event_name': 'AccountDeleted',
            'data': {
                'public_id': str(uuid),
            }
        }
    produce_message('accounts-stream', event)    

def produce_role_changed_event(account):
    event = {
            'event_name': 'AccountRoleChanged',
            'data': {
                'public_id': str(account.uuid),
                'role': account.role,
            }
        }
    produce_message('accounts', event)
