from netbox.plugins import PluginConfig


class Config(PluginConfig):
    name = 'netbox_ping'
    verbose_name = 'NetBox Ping'
    description = 'Ping IPs and subnets'
    version = '0.2'
    author = 'Your Name'
    author_email = 'your.email@example.com'
    default_settings = {
        'exclude_virtual_interfaces': True
    }
    template_content = 'netbox_ping.template_content.template_content'


config = Config