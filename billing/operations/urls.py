from django.urls import path
from .views import BalanceViewSet



urlpatterns = [
    path('balance/<int:account_pk>/today-log/', BalanceViewSet.as_view({'get': 'today_log'}), name='today_log'),
    path('balance/today_money/', BalanceViewSet.as_view({'get': 'today_money'}), name='today_money'),
]
