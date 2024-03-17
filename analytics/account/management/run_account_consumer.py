from django.core.management.base import BaseCommand
from billing.account.consumer import consume_messages
import logging
log = logging.getLogger('cron')

class Command(BaseCommand):
    command_name = 'consume topic messages'
    def add_arguments(self, parser):        
        parser.add_argument('--topic', type=str, help='Name of the topic to consume', rewuired=True)
    
    def handle(self, *args, **options):
        log.info(f'Start {self.command_name}')
        topic = options['topic']
        consume_messages(topic)
        log.info(f'End {self.command_name}')
