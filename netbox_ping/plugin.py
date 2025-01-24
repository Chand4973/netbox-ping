from netbox.plugins import PluginConfig

class NetBoxPingConfig(PluginConfig):
    name = 'netbox_ping'
    verbose_name = 'NetBox Ping'
    description = 'Ping IPs or subnets in NetBox'
    version = '0.2'
    base_url = 'ping'

config = NetBoxPingConfig