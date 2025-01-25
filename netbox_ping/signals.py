from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from extras.choices import CustomFieldTypeChoices
from extras.models import CustomField, Tag

@receiver(post_migrate)
def create_custom_fields_and_tags(sender, **kwargs):
    """
    Create required custom fields and tags after database migrations complete
    """
    if sender.name == 'netbox_ping':
        # Create Up_Down custom field
        custom_field, _ = CustomField.objects.get_or_create(
            name='Up_Down',
            defaults={
                'type': CustomFieldTypeChoices.TYPE_BOOLEAN,
                'label': 'Up/Down Status',
                'description': 'Indicates if the IP is responding to ping',
                'required': False,
                'filter_logic': 'exact'
            }
        )
        
        # Add the custom field to IPAddress content type
        ipaddress_ct = ContentType.objects.get_for_model(apps.get_model('ipam', 'ipaddress'))
        if ipaddress_ct not in custom_field.content_types.all():
            custom_field.content_types.add(ipaddress_ct)

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