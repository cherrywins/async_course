from django.core.management.base import BaseCommand
from billing.task.consumer import consume_messages, process_assign_message_v1, process_complete_message_v1
import logging
from datetime import datetime
from billing.task.models import DeadQueueTaskEvent
log = logging.getLogger('cron')

class Command(BaseCommand):
    command_name = 'run tasks dead queue'
    
    def handle(self, *args, **options):
        log.info(f'Start {self.command_name}')
        unsync_events = DeadQueueTaskEvent.objects.filter(sync_at__isnull=True).order_by('timestamp')
        for event in unsync_events:
            if (
                event.name == 'TaskCompleted' and
                unsync_events.filter(timestamp__lte=event.timestamp).exists()
            ):
                continue
            try:
                if event.name == 'TaskCompleted':
                    process_complete_message_v1(event.data)
                elif event.name == 'TaskAssigned':
                    process_assign_message_v1(event.data)
                event.sync_at = datetime.now()
            except ValueError:
                event.atempts += 1
            finally:
                event.save()       
        log.info(f'End {self.command_name}')
