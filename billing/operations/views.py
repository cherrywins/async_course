from django.db.models import QuerySet
from rest_framework.decorators import action
from account.models import Account
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from datetime import datetime
from django.db.models import Sum

from operations.models import OperationLog


class BalanceViewSet(viewsets.GenericViewSet):
    queryset = Account.objects.all()
    
    def get_queryset(self) -> QuerySet:
        return self.queryset.filter(
            id=self.kwargs["account_pk"],
        )
        
    @action(detail=True, methods=["get"])
    def today_log(self, request, *args, **kwargs):
        account: Account = self.get_object()
        now = datetime.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now
        today_balance = 0
        data_out = {'logs': []}
        data_out['total_balance'] = account.balance
        logs = OperationLog.objects.filter(
            account=account,
            date__gte=start_of_day,
            date_lte=end_of_day,
        ).order_by('date')
        for log in logs:
           data_out['logs'].append({
               'type': log.operation_type,
               'amount': log.amount,
               'task': log.task_title,
               'date': log.date,
           }) 
           today_balance += log.amount
        data_out['today_balance'] = today_balance
        return Response({"data": data_out}, status.HTTP_200_OK)
    
    
    @action(detail=False, methods=["get"])
    def today_money(self, request, *args, **kwargs):
        now = datetime.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now
        charge_total = OperationLog.objects.filter(
            date__gte=start_of_day,
            date__lte=end_of_day,
            operation_type='charge'
        ).aggregate(total_charge=Sum('amount'))['total_charge']

        reward_total = OperationLog.objects.filter(
            date__gte=start_of_day,
            date__lte=end_of_day,
            operation_type='reward'
        ).aggregate(total_reward=Sum('amount'))['total_reward']
        
        data_out = {
            'charge_total': charge_total,
            'reward_total': reward_total,
            'balance': charge_total - reward_total,
        }
        
        return Response({"data": data_out}, status.HTTP_200_OK)
