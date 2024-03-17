from django.urls import path
from .views import LoginView

urlpatterns = [
    path('billing_login/', LoginView.as_view(), name='billing_login'),  
]
