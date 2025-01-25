from django import forms
from netbox.forms import NetBoxModelForm
from .models import PluginSettingsModel


class InterfaceComparisonForm(forms.Form):
    add_to_device = forms.BooleanField(required=False)
    remove_from_device = forms.BooleanField(required=False)

class PluginSettingsForm(NetBoxModelForm):
    class Meta:
        model = PluginSettingsModel
        fields = ('update_tags',)