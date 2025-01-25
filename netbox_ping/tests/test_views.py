import pytest
from django.urls import reverse
from netbox.tests import TestCase
from ..models import PluginSettingsModel

class TestPingHomeView(TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('plugins:netbox_ping:ping_home')

    def test_ping_home_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class TestPluginSettings(TestCase):
    def test_settings_model(self):
        settings = PluginSettingsModel.get_settings()
        self.assertTrue(hasattr(settings, 'update_tags'))
        self.assertTrue(isinstance(settings.update_tags, bool)) 