import pytest
from django.urls import reverse
from netbox.tests import TestCase
from ..models import PluginSettingsModel
from users.models import User

class TestPingHomeView(TestCase):
    def setUp(self):
        super().setUp()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('plugins:netbox_ping:ping_home')

    def test_ping_home_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_ping_home_view_with_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class TestPluginSettings(TestCase):
    def test_settings_model(self):
        settings = PluginSettingsModel.get_settings()
        self.assertTrue(hasattr(settings, 'update_tags'))
        self.assertTrue(isinstance(settings.update_tags, bool)) 