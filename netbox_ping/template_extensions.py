# netbox_ping/template_extensions.py

import logging
from netbox.plugins import PluginTemplateExtension
from ipam.models import Prefix, IPAddress
from django.urls import reverse

logger = logging.getLogger(__name__)

class PrefixButtonsExtension(PluginTemplateExtension):
    model = 'ipam.prefix'

    def buttons(self):
        prefix = self.context["object"]
        ping_url = reverse('netbox_ping:pingprefix', kwargs={'pk': prefix.pk})
        logger.debug(f"Rendering Ping Subnet button for Prefix ID: {prefix.pk}")
        return [
            self.render('netbox_ping/prefix_button.html', {
                'ping_url': ping_url
            })
        ]

class IPAddressButtonsExtension(PluginTemplateExtension):
    model = 'ipam.ipaddress'

    def buttons(self):
        ip_address = self.context["object"]
        ping_url = reverse('netbox_ping:pingip', kwargs={'pk': ip_address.pk})
        logger.debug(f"Rendering Ping IP button for IPAddress ID: {ip_address.pk}")
        return [
            self.render('netbox_ping/ip_button.html', {
                'ping_url': ping_url
            })
        ]

template_extensions = [PrefixButtonsExtension, IPAddressButtonsExtension]
