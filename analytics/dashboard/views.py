import requests
from datetime import datetime
from django.db.models import Max

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from analytics.dashboard.models import PayOutLog
from analytics.task.models import Task


class DashboardViewSet(viewsets.GenericViewSet):
    
    @action(detail=False, methods=["get"])
    def today_money(self, request, *args, **kwargs):
        url = 'http://127.0.0.1:8000/balance/today_money'
        response = requests.get(url)
        data_out = response.json()
        now = datetime.now()
        
        # сколько попугов ушло в минус = скольким попугам мы ничего не выплатили
        today_zero_payouts = PayOutLog.objects.filter(date=now.date(), amount=0).count()
        
        data_out['today_zero_payouts'] = today_zero_payouts
        
        return Response({"data": data_out}, status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"])
    def tasks_analytics(self, request, *args, **kwargs):
        data_out = {}
        tasks_with_date_completed = Task.objects.filter(date_completed__isnull=False)
        grouped_tasks = tasks_with_date_completed.values('date_completed')
        grouped_tasks = grouped_tasks.annotate(max_reward=Max('reward'))
        most_expensive_tasks = grouped_tasks.order_by('-max_reward')
        for task in most_expensive_tasks:
            data_out[task['date_completed']] = task['max_reward']
        return Response({"data": data_out}, status.HTTP_200_OK)
        
