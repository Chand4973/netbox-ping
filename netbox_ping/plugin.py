from django.contrib.contenttypes.models import ContentType
from extras.api.serializers import CustomFieldSerializer, TagSerializer
from extras.models import CustomField, Tag
from ipam.models import IPAddress
from rest_framework.exceptions import ValidationError

def initialize_plugin():
    """Initialize plugin custom fields and tags using the API"""
    
    # Get ContentType ID for IPAddress
    ipaddress_ct_id = ContentType.objects.get_for_model(IPAddress).id
    
    # Create Up_Down custom field
    up_down_data = {
        'name': 'Up_Down',
        'type': 'boolean',
        'label': 'Up/Down Status',
        'description': 'Indicates if the IP is responding to ping',
        'required': False,
        'filter_logic': 'exact',
        'ui_visible': 'always',
        'ui_editable': 'yes',
        'is_cloneable': True,
        'weight': 100,
    }
    
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
    for cf_data in [up_down_data, discovered_data]:
        try:
            custom_field = CustomField.objects.get(name=cf_data['name'])
        except CustomField.DoesNotExist:
            try:
                custom_field = CustomField.objects.create(**cf_data)
                custom_field.object_types.set([ipaddress_ct_id])
                print(f"Created custom field: {custom_field.name}")
            except Exception as e:
                print(f"Failed to create custom field: {str(e)}")

    # Create tags
    tags_data = [
        {
            'name': 'online',
            'slug': 'online',
            'description': 'IP is responding to ping',
            'color': '4CAF50'
        },
        {
            'name': 'offline',
            'slug': 'offline',
            'description': 'IP is not responding to ping',
            'color': 'F44336'
        },
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