from confluent_kafka import Producer

def produce_message(topic_name, message):
    p = Producer({'bootstrap.servers': 'localhost:9092'})
    p.produce(topic_name, message)
    p.flush()

def produce_create_event(data):
    event = {
            'event_name': 'AccountCreated',
            'data': {
                'public_id': data['uuid'],
                'email': data['email'],
                'name': data['name'],
                'role': data['role'],
            }
        }
    produce_message('accounts-stream', event)

def produce_update_event(data):
    event = {
            'event_name': 'AccountUpdated',
            'data': {
                'public_id': data['uuid'],
                'email': data['email'],
                'name': data['name'],
                'role': data['role'],
            }
        }
    produce_message('accounts-stream', event)    

def produce_delete_event(pk):
    event = {
            'event_name': 'AccountDeleted',
            'data': {
                'public_id': pk,
            }
        }
    produce_message('accounts-stream', event)    

def produce_role_changed_event(data):
    event = {
            'event_name': 'AccountRoleChanged',
            'data': {
                'public_id': data['uuid'],
                'role': data['role'],
            }
        }
    produce_message('accounts', event)
