import uuid
from billing.account.models import Account
from datetime import datetime

from billing.operations.models import PayOutLog
from billing.operations.producer import produce_payout_log_event

def create_daily_payout(account: Account, pay_out_summ: int):
    now = datetime.now()
    payout = PayOutLog.objects.create(
        account=account,
        amount=pay_out_summ,
        date=now.date(),
        uuid=uuid.uuid4(),
    )
    produce_payout_log_event(payout)
