from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from ..models import PluginSettingsModel

class PluginSettingsModelSerializer(NetBoxModelSerializer):
    class Meta:
        model = PluginSettingsModel
        fields = (
            'id', 'update_tags', 'dns_server1', 'dns_server2', 
            'dns_server3', 'perform_dns_lookup', 'created', 
            'last_updated'
        )
        brief_fields = ['id', 'update_tags'] 