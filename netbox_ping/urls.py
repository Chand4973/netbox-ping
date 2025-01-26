from django.urls import path

from . import views

app_name = 'netbox_ping'

# Define a list of URL patterns to be imported by NetBox. Each pattern maps a URL to
# a specific view so that it can be accessed by users.
urlpatterns = [
    path('', views.PingHomeView.as_view(), name='ping_home'),
    path('ping-subnet/<int:prefix_id>/', views.PingSubnetView.as_view(), name='ping_subnet'),
    path('scan-subnet/<int:prefix_id>/', views.ScanSubnetView.as_view(), name='scan_subnet'),
    path('initialize/', views.InitializePluginView.as_view(), name='initialize_plugin'),
    path('scan-all/', views.ScanAllView.as_view(), name='scan_all'),
    path('update-settings/', views.UpdateSettingsView.as_view(), name='update_settings'),
    path('ping-ip/<str:ip_address>/', views.PingSingleIPView.as_view(), name='ping_ip'),
    path('scan-prefix/<str:prefix>/', views.ScanSinglePrefixView.as_view(), name='scan_prefix'),
]