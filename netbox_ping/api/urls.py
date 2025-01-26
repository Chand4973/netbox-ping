from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox-ping-api'

router = NetBoxRouter()
router.register('settings', views.PluginSettingsViewSet)

urlpatterns = router.urls 