import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import autoreload

from account.consumer_command import consume_messages

class Command(BaseCommand):
    def handle(self, *args, **options):
        # consume_messages('accounts-stream')
        consume_messages('accounts')
        pass
