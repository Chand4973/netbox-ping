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

    def __str__(self):
        return "NetBox Ping Settings"

    @classmethod
    def get_settings(cls):
        """Get or create settings"""
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings 