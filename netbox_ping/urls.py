# netbox_ping/urls.py

from django.urls import path
from .views import PingPrefixView, PingIPAddressView

app_name = 'netbox_ping'

urlpatterns = [
    path('ping-prefix/<int:pk>/', PingPrefixView.as_view(), name='pingprefix'),
    path('ping-ip/<int:pk>/', PingIPAddressView.as_view(), name='pingip'),
]
