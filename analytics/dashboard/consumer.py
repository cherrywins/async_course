from confluent_kafka import Consumer, KafkaException

from billing.operations.charge import charge_assignee
from billing.operations.reward import reward_assignee
from .models import Account, DeadQueueTaskEvent, PayOutLog, Task
import json
from jsonschema import validate
from .schemes import pay_out_schema_v1
import logging
from datetime import datetime

import random
log = logging.getLogger('billing_task_consumer')
    
def process_payout_message_v1(message):
    payout = PayOutLog.objects.create(
        uuid=message['data']['payout_id'],
        account_id=message['data']['account_id'],
        amount=message['data']['amount'],
        date=datetime.strptime(message['data']['amount'], '%m/%d/%y %H:%M:%S')
    )
    payout.save()

def validate_and_process_payout_event(message):
    """
        Creation and update of tasks
    """
    print(f"Processing message: {message}")
    message = json.loads(message)
    try:
        if message['event_name'] == 'DailyPayOut':
            validate(message, pay_out_schema_v1)
            process_payout_message_v1(message)
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
        if topic_name == 'payout':
            validate_and_process_payout_event(msg.value().decode('utf-8'))
    consumer.close()
