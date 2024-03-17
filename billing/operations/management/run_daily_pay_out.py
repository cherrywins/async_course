import logging
import uuid

from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.models import Sum

from billing.account.models import Account
from billing.account.utils import send_email_to_account
from billing.operations.models import OperationLog, PayOutLog
from billing.operations.utils import create_daily_payout


log = logging.getLogger('cron')

class Command(BaseCommand):
    command_name = 'daily pay out'    
    def handle(self, *args, **options):
        log.info(f'Start {self.command_name}')
        now = datetime.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        logs = OperationLog.objects.filter(
            date__gte=start_of_day,
            date_lte=now,
        )
        account_ids = logs.distinct('account').values_list('account_id', flat=True)
        accounts = Account.object.filter(id__in=account_ids)
        
        for account in accounts:
            logs = logs.filter(account=self)
            total_earned_today = logs.aggregate(total_amount=Sum('amount'))['total_amount']
            current_balance = account.balance
            new_balance =  current_balance + total_earned_today
            if new_balance > 0:
                pay_out_summ = new_balance
                account.balance = 0
            else:
                pay_out_summ = 0
            account.save()
            logs.update(is_processed=True)
            create_daily_payout(account, pay_out_summ)
            send_email_to_account(account, total_earned_today, pay_out_summ)
        
        log.info(f'End {self.command_name}')
