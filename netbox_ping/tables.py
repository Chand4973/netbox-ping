import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from ipam.models import IPAddress
from ipam.tables import IPAddressTable

class CustomIPAddressTable(IPAddressTable):
    """Custom IP Address table that includes the Up_Down status"""
    
    up_down = columns.BooleanColumn(
        verbose_name='Ping Status',
        accessor=tables.A('_custom_field_data__Up_Down'),
        order_by='_custom_field_data__Up_Down',
    )

    online = columns.TagColumn(
        verbose_name='Online/Offline'
    )

    class Meta(IPAddressTable.Meta):
        model = IPAddress
        fields = IPAddressTable.Meta.fields + ('up_down', 'online')
        default_columns = ('address', 'status', 'up_down', 'online', 'tenant', 'assigned_object', 'description') 