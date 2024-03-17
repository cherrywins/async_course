from django.urls import path
from .views import LoginView

urlpatterns = [
    path('analytics_login/', LoginView.as_view(), name='billing_login'),  
]
