from netbox.plugins import PluginMenuItem, PluginMenuButton

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_ping:ip_pinger',
        link_text='IP Pinger',
        permissions=('ipam.view_prefix',),
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_ping:ip_pinger',
                title='IP Pinger',
                icon_class='mdi mdi-target',
                permissions=('ipam.view_prefix',),
            ),
        ),
    ),
)
