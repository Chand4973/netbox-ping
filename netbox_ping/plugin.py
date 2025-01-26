from django.contrib.contenttypes.models import ContentType
from extras.api.serializers import CustomFieldSerializer, TagSerializer
from extras.models import CustomField, Tag, CustomLink
from ipam.models import IPAddress, Prefix
from rest_framework.exceptions import ValidationError
from extras.choices import CustomFieldTypeChoices
from core.models import ObjectType

def initialize_plugin():
    """Initialize plugin settings."""
    
    # Create required tags
    online_tag, _ = Tag.objects.get_or_create(
        name='online',
        defaults={
            'description': 'Device is online',
            'color': '4CAF50'  # Green
        }
    )

    offline_tag, _ = Tag.objects.get_or_create(
        name='offline',
        defaults={
            'description': 'Device is offline',
            'color': 'F44336'  # Red
        }
    )

    auto_discovered_tag, _ = Tag.objects.get_or_create(
        name='auto-discovered',
        defaults={
            'description': 'IP was automatically discovered',
            'color': '2196F3'  # Blue
        }
    )

    # Get the content types we need
    ipaddress_ct = ContentType.objects.get(app_label='ipam', model='ipaddress')
    prefix_ct = ContentType.objects.get(app_label='ipam', model='prefix')
    
    # Create "Ping" button for IP Address pages
    link, _ = CustomLink.objects.get_or_create(
        name='Ping IP',
        link_text='Ping',
        link_url='plugins/netbox-ping/ping-ip/{{ object.address }}/',
        weight=100
    )
    ipaddress_type = ObjectType.objects.get(app_label='ipam', model='ipaddress')
    link.object_types.add(ipaddress_type)

    # Create "Ping Subnet" button for Prefix pages
    link, _ = CustomLink.objects.get_or_create(
        name='Ping Subnet',
        link_text='Ping Subnet',
        link_url='plugins/netbox-ping/scan-prefix/{{ object.prefix }}/?action=ping',
        weight=100
    )
    prefix_type = ObjectType.objects.get(app_label='ipam', model='prefix')
    link.object_types.add(prefix_type)

    # Create "Discover IPs" button for Prefix pages
    link, _ = CustomLink.objects.get_or_create(
        name='Discover IPs',
        link_text='Discover IPs',
        link_url='plugins/netbox-ping/scan-prefix/{{ object.prefix }}/?action=scan',
        weight=200
    )
    link.object_types.add(prefix_type)

    # Create Up_Down custom field
    up_down_field, _ = CustomField.objects.get_or_create(
        name='Up_Down',
        defaults={
            'type': CustomFieldTypeChoices.TYPE_BOOLEAN,
            'label': 'Up/Down Status',
            'description': 'Current up/down status of the IP',
        }
    )

    # Get IPAddress content type
    ipaddress_ct = ContentType.objects.get(app_label='ipam', model='ipaddress')

    # Add content type to custom fields
    if not up_down_field.object_types.filter(id=ipaddress_ct.id).exists():
        up_down_field.object_types.add(ipaddress_ct)

    # Create custom fields
    dns_name_field, _ = CustomField.objects.get_or_create(
        name='dns_name',
        defaults={
            'type': CustomFieldTypeChoices.TYPE_TEXT,
            'label': 'DNS Name',
            'description': 'Resolved DNS name for this IP',
        }
    )

    # Add content type to custom fields
    for field in [up_down_field, dns_name_field]:
        if not field.object_types.filter(id=ipaddress_ct.id).exists():
            field.object_types.add(ipaddress_ct)

    # Create Auto_discovered custom field
    discovered_data = {
        'name': 'Auto_discovered',
        'type': 'date',
        'label': 'Auto Discovered',
        'description': 'Date when this IP was automatically discovered',
        'required': False,
        'filter_logic': 'exact',
        'ui_visible': 'always',
        'ui_editable': 'yes',
        'is_cloneable': True,
        'weight': 101,
    }

    # Create custom fields
    for cf_data in [discovered_data]:
        try:
            custom_field = CustomField.objects.get(name=cf_data['name'])
        except CustomField.DoesNotExist:
            try:
                custom_field = CustomField.objects.create(**cf_data)
                custom_field.object_types.set([ipaddress_ct.id])
                print(f"Created custom field: {custom_field.name}")
            except Exception as e:
                print(f"Failed to create custom field: {str(e)}")

    # Create tags
    tags_data = [
        {
            'name': 'auto-discovered',
            'slug': 'auto-discovered',
            'description': 'IP was automatically discovered by scanning',
            'color': '2196F3'  # Blue color
        }
    ]
    
    for tag_data in tags_data:
        try:
            tag = Tag.objects.get(slug=tag_data['slug'])
        except Tag.DoesNotExist:
            try:
                tag = Tag.objects.create(**tag_data)
                print(f"Created tag: {tag.name}")
            except Exception as e:
                print(f"Failed to create tag: {str(e)}") 