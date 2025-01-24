# netbox_ping/netbox_ping/template_extensions.py

from netbox.views.template_extensions import TemplateExtension

class PrefixButtons(TemplateExtension):
    model = 'ipam.prefix'

    def buttons(self):
        prefix = self.context["object"]
        url = f"/plugins/ping/ping-prefix/{prefix.pk}/"
        return self.render('netbox_ping/prefix_button.html', {'ping_url': url})
