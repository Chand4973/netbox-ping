from django.urls import path

from . import views

app_name = 'netbox_ping'

# Define a list of URL patterns to be imported by NetBox. Each pattern maps a URL to
# a specific view so that it can be accessed by users.
urlpatterns = (
    path('', views.PingHomeView.as_view(), name='ping_home'),
    path('ping-subnet/<int:prefix_id>/', views.PingSubnetView.as_view(), name='ping_subnet'),
    path('scan-subnet/<int:prefix_id>/', views.ScanSubnetView.as_view(), name='scan_subnet'),
)