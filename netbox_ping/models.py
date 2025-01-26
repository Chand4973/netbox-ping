from django.db import models
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet

class PluginSettingsModel(NetBoxModel):
    """Store plugin settings"""
    class Meta:
        verbose_name = 'Plugin Settings'
        verbose_name_plural = 'Plugin Settings'
        ordering = ['pk']

    # Required fields from NetBoxModel
    id = models.BigAutoField(
        primary_key=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )
    custom_field_data = models.JSONField(
        blank=True,
        null=True,
        default=dict
    )

    # Our custom fields
    update_tags = models.BooleanField(
        default=True,
        verbose_name='Update Tags',
        help_text='Whether to update tags when scanning IPs'
    )

    # Add DNS server fields
    dns_server1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Primary DNS Server',
        help_text='Primary DNS server (e.g., 8.8.8.8)'
    )

    dns_server2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Secondary DNS Server',
        help_text='Secondary DNS server (e.g., 8.8.4.4)'
    )

    dns_server3 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Tertiary DNS Server',
        help_text='Tertiary DNS server'
    )

    perform_dns_lookup = models.BooleanField(
        default=True,
        verbose_name='Perform DNS Lookups',
        help_text='Whether to perform DNS lookups when scanning IPs'
    )

    def __str__(self):
        return "NetBox Ping Settings"

    @classmethod
    def get_settings(cls):
        """Get or create settings"""
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings 