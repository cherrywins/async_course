from confluent_kafka import Consumer, KafkaException
from .models import Account
from task.utils import reassign_tasks
import json

def process_message(message):
    print(f"Processing message: {message}")
    message = json.loads(message)
    if message["event_name"] == "AccountCreated":
        Account.objects.create(
            uuid=message['data']['public_id'],
            email=message['data']['email'],
            name=message['data']['name'],
            role=message['data']['role'],
        )
    elif message["event_name"] == "AccountUpdated":
        account = Account.objects.get(uuid=message['data']['public_id'])
        account.email=message['data']['email']
        account.name=message['data']['name']
        account.role=message['data']['role']
        account.save()
    elif message["event_name"] == "AccountDeleted":
        account = Account.objects.get(uuid=message['data']['public_id'])
        account.delete()
    elif message["event_name"] == "AccountRoleChanged":
        account = Account.objects.get(uuid=message['data']['public_id'])
        prev_account_role = account.role
        account.role=message['data']['role']
        if prev_account_role != message['data']['role'] and message['data']['role'] in ['manager', 'admin']:
            reassign_tasks()
        account.save()
    

def consume_messages(topic_name):
    c = Consumer({
        'bootstrap.servers': 'localhost:9094',
        'group.id': 'tasks-consumer-group',
        'auto.offset.reset': 'earliest'
    })

    c.subscribe([topic_name])

    n = 3
    while n > 0:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            process_message(msg.value().decode('utf-8'))
        n = n - 1
    c.close()
