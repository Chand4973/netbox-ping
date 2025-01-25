from extras.choices import CustomFieldTypeChoices
from extras.models import CustomField, Tag
from django.db.models import Q

def create_custom_fields_and_tags():
    """Create custom fields and tags needed by the plugin"""
    
    # Create Up_Down custom field
    custom_field, created = CustomField.objects.get_or_create(
        name='Up_Down',
        defaults={
            'type': CustomFieldTypeChoices.TYPE_BOOLEAN,
            'label': 'Up/Down Status',
            'description': 'Indicates if the IP is responding to ping',
            'required': False,
            'filter_logic': 'exact'
        }
    )
    
    # Add the custom field to IPAddress content type if not already added
    if created:
        custom_field.content_types.add(
            ContentType.objects.get(app_label='ipam', model='ipaddress')
        )

    # Create online/offline tags
    Tag.objects.get_or_create(
        name='online',
        slug='online',
        defaults={
            'description': 'IP is responding to ping',
            'color': '4CAF50'  # Green color
        }
    )

    Tag.objects.get_or_create(
        name='offline',
        slug='offline',
        defaults={
            'description': 'IP is not responding to ping',
            'color': 'F44336'  # Red color
        }
    ) 