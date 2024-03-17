from confluent_kafka import Producer
import json
import uuid
import time
from jsonschema import validate
from .schemes import pay_out_schema_v1

def produce_message(topic_name, message):
    p = Producer({'bootstrap.servers': 'localhost:9094'})
    p.produce(topic_name, json.dumps(message))
    p.flush()

def produce_payout_log_event(payout):
    event = {
            'metadata': {
                'version': 1,
                'event_name': 'DailyPayOut',
                'event_uuid': uuid.uuid4(),
                'timestamp': time.time()
            },
            'data': {
                'payout_id': str(payout.uuid),
                'account_id': str(payout.account.uuid),
                'amount': payout.amount,
                'date': payout.date(),
            }
        }
    validate(event, pay_out_schema_v1)
    produce_message('payout', event)

    
    
