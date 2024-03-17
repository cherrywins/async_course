from confluent_kafka import Consumer, KafkaException
from .models import Account
import json
from jsonschema import validate
from .schemes import account_stream_schema_v1, account_stream_schema_v2

def process_message_v1(message):
    if message["event_name"] == "AccountCreated":
        Account.objects.create(
            uuid=message['data']['public_id'],
            email=message['data']['email'],
            name=message['data']['name'],
            role=message['data']['role'],
        )
    elif message["event_name"] == "AccountUpdated":
        account = Account.objects.filter(uuid=message['data']['public_id']).first()
        if not account:
            account = Account(uuid=message['data']['public_id'])
        account.email=message['data']['email']
        account.name=message['data']['name']
        account.role=message['data']['role']

    account.save()
    
def process_message_v2(message):
    if message["metadata"]["event_name"] == "AccountCreated":
        Account.objects.create(
            uuid=message['data']['account_id'],
            email=message['data']['email'],
            name=message['data']['name'],
            role=message['data']['role'],
            balance=0,
        )
    elif message["metadata"]["event_name"] == "AccountUpdated":
        account = Account.objects.filter(uuid=message['data']['account_id']).first()
        if not account:
            raise ValueError('The account does not exist')
        account.email=message['data']['email']
        account.name=message['data']['name']
        account.role=message['data']['role']
    account.save()
    

def process_message_accounts_stream(message):
    print(f"Processing message: {message}")
    message = json.loads(message)
    try:
        validate(message, account_stream_schema_v2)
        process_message_v2(message)
    except Exception:
        validate(message, account_stream_schema_v1)
        process_message_v1(message)
    

def consume_messages(topic_name):
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9094',
        'group.id': 'tasks-consumer-group',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([topic_name])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            break
        if msg.error():
            raise KafkaException(msg.error())
        else:
            if topic_name == 'accounts-stream':
                process_message_accounts_stream(msg.value().decode('utf-8'))
    consumer.close()
