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
    # Producer.call(event, topic='accounts-stream')

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
    # Producer.call(event, topic='accounts-stream')
    

def produce_delete_event(pk):
    event = {
            'event_name': 'AccountDeleted',
            'data': {
                'public_id': pk,
            }
        }
    # Producer.call(event, topic='accounts-stream')
    

def produce_role_changed_event(data):
    event = {
            'event_name': 'AccountRoleChanged',
            'data': {
                'public_id': data['uuid'],
                'role': data['role'],
            }
        }
    # Producer.call(event, topic='accounts')
