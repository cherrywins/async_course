from django.urls import path
from .views import InfoView, TokenView

urlpatterns = [
    path('token/', TokenView.as_view(), name='token'),
    path('account_info/', InfoView.as_view(), name='account_info'),
]
