# netbox_ping/plugin.py

from netbox.plugins import PluginConfig

class NetBoxPingConfig(PluginConfig):
    name = 'netbox_ping'
    verbose_name = 'NetBox Ping'
    description = 'Ping IPs and subnets'
    version = '0.2'
    base_url = 'ping'
    template_extension_path = 'netbox_ping.template_extensions'

config = NetBoxPingConfig
