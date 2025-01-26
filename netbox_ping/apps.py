from django.apps import AppConfig

class NetBoxPingConfig(AppConfig):
    name = 'netbox_ping'
    verbose_name = 'NetBox Ping'
    default = True

    def ready(self):
        from . import signals 