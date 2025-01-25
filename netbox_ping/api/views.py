from netbox.api.viewsets import NetBoxModelViewSet
from .. import models
from .serializers import PluginSettingsModelSerializer

class PluginSettingsViewSet(NetBoxModelViewSet):
    queryset = models.PluginSettingsModel.objects.all()
    serializer_class = PluginSettingsModelSerializer 