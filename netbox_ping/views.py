# netbox_ping/netbox_ping/views.py

import subprocess
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from ipam.models import Prefix, IPAddress

class PingPrefixView(View):
    def get(self, request, pk):
        prefix = get_object_or_404(Prefix, pk=pk)
        # Placeholder for actual ping-sweep logic
        messages.success(request, f"Ping-sweep stub for {prefix} done!")
        return redirect(prefix.get_absolute_url())

class PingIPAddressView(View):
    def get(self, request, pk):
        ip = get_object_or_404(IPAddress, pk=pk)
        cmd = ['ping', '-c', '1', str(ip.address.ip)]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                messages.success(request, f"IP {ip.address} is online!")
            else:
                messages.warning(request, f"IP {ip.address} did not respond.")
        except subprocess.TimeoutExpired:
            messages.error(request, f"Ping to IP {ip.address} timed out.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect(ip.get_absolute_url())
