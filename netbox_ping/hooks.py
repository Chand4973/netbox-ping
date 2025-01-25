from extras.plugins import PluginTemplateExtension
from . import tables

def override_ipaddress_table():
    """Override the default IP address table to include Up_Down status"""
    return tables.CustomIPAddressTable 