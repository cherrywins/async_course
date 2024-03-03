from django.urls import path
from .views import AccountView

urlpatterns = [
    path('accounts/', AccountView.as_view(), name='accounts'),  
    path('accounts/<uuid:pk>/', AccountView.as_view(), name='account_detail'),
]
