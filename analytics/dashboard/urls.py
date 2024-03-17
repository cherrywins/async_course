from django.urls import path
from .views import BalanceViewSet, DashboardViewSet



urlpatterns = [
    path('dashboard/<int:account_pk>/today-log/', BalanceViewSet.as_view({'get': 'today_log'}), name='today_log'),
    path('dashboard/today_money/', DashboardViewSet.as_view({'get': 'today_money'}), name='today_money'),
]
