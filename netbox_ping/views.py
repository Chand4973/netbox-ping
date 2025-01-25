from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from dcim.models import Device, Interface, InterfaceTemplate
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.conf import settings
from django.contrib import messages
from ipam.models import Prefix, IPAddress
from ipaddress import ip_network, ip_interface
import subprocess
import concurrent.futures

from .utils import UnifiedInterface, natural_keys
from .forms import InterfaceComparisonForm
from extras.models import Tag

config = settings.PLUGINS_CONFIG['netbox_ping']


class InterfaceComparisonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Comparison of interfaces between a device and a device type and beautiful visualization"""
    permission_required = ("dcim.view_interface", "dcim.add_interface", "dcim.change_interface", "dcim.delete_interface")

    def get(self, request, device_id):
        device = get_object_or_404(Device.objects.filter(id=device_id))
        interfaces = device.vc_interfaces()
        if config["exclude_virtual_interfaces"]:
            interfaces = list(filter(lambda i: not i.is_virtual, interfaces))
        interface_templates = InterfaceTemplate.objects.filter(device_type=device.device_type)

        unified_interfaces = [UnifiedInterface(i.id, i.name, i.type, i.get_type_display()) for i in interfaces]
        unified_interface_templates = [
            UnifiedInterface(i.id, i.name, i.type, i.get_type_display(), i.mgmt_only, is_template=True) for i in interface_templates]

        # List of interfaces and interface templates presented in the unified format
        overall_interfaces = list(set(unified_interface_templates + unified_interfaces))
        overall_interfaces.sort(key=lambda o: natural_keys(o.name))

        comparison_templates = []
        comparison_interfaces = []
        for i in overall_interfaces:
            try:
                comparison_templates.append(unified_interface_templates[unified_interface_templates.index(i)])
            except ValueError:
                comparison_templates.append(None)

            try:
                comparison_interfaces.append(unified_interfaces[unified_interfaces.index(i)])
            except ValueError:
                comparison_interfaces.append(None)

        comparison_items = list(zip(comparison_templates, comparison_interfaces))
        return render(
            request, "netbox_ping/interface_comparison.html",
            {
                "comparison_items": comparison_items,
                "templates_count": len(interface_templates),
                "interfaces_count": len(interfaces),
                "device": device
             }
        )

    def post(self, request, device_id):
        form = InterfaceComparisonForm(request.POST)
        if form.is_valid():
            device = get_object_or_404(Device.objects.filter(id=device_id))
            interfaces = device.vc_interfaces()
            if config["exclude_virtual_interfaces"]:
                interfaces = interfaces.exclude(type__in=["virtual", "lag"])
            interface_templates = InterfaceTemplate.objects.filter(device_type=device.device_type)

            # Manually validating interfaces and interface templates lists
            add_to_device = filter(
                lambda i: i in interface_templates.values_list("id", flat=True),
                map(int, filter(lambda x: x.isdigit(), request.POST.getlist("add_to_device")))
            )
            remove_from_device = filter(
                lambda i: i in interfaces.values_list("id", flat=True),
                map(int, filter(lambda x: x.isdigit(), request.POST.getlist("remove_from_device")))
            )

            # Remove selected interfaces from the device and count them
            interfaces_deleted = Interface.objects.filter(id__in=remove_from_device).delete()[0]

            # Add selected interfaces to the device and count them
            add_to_device_interfaces = InterfaceTemplate.objects.filter(id__in=add_to_device)
            interfaces_created = len(Interface.objects.bulk_create([
                Interface(device=device, name=i.name, type=i.type, mgmt_only=i.mgmt_only) for i in add_to_device_interfaces
            ]))

            # Getting and validating a list of interfaces to rename
            fix_name_interfaces = filter(lambda i: str(i.id) in request.POST.getlist("fix_name"), interfaces)
            # Casting interface templates into UnifiedInterface objects for proper comparison with interfaces for renaming
            unified_interface_templates = [
                UnifiedInterface(i.id, i.name, i.type,i.mgmt_only, i.get_type_display()) for i in interface_templates]

            # Rename selected interfaces
            interfaces_fixed = 0
            for interface in fix_name_interfaces:
                unified_interface = UnifiedInterface(interface.id, interface.name, interface.type, interface.mgmt_only, interface.get_type_display())
                try:
                    # Try to extract an interface template with the corresponding name
                    corresponding_template = unified_interface_templates[unified_interface_templates.index(unified_interface)]
                    interface.name = corresponding_template.name
                    interface.save()
                    interfaces_fixed += 1
                except ValueError:
                    pass

            # Generating result message
            message = []
            if interfaces_created > 0:
                message.append(f"created {interfaces_created} interfaces")
            if interfaces_deleted > 0:
                message.append(f"deleted {interfaces_deleted} interfaces")
            if interfaces_fixed > 0:
                message.append(f"fixed {interfaces_fixed} interfaces")
            messages.success(request, "; ".join(message).capitalize())

            return redirect(request.path)

class PingHomeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "ipam.view_prefix"

    def get(self, request):
        return render(request, 'netbox_ping/ping_home.html', {
            'prefixes': Prefix.objects.all(),
            'tab': 'main',
            'model': Prefix,
            'table': None,
            'actions': ('add', 'import', 'export', 'bulk_edit', 'bulk_delete'),
        })

class PingSubnetView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """View for pinging existing IPs in a subnet"""
    permission_required = "ipam.view_prefix"

    def ping_ip(self, ip):
        """Ping a single IP address"""
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], 
                                  capture_output=True, 
                                  timeout=2)
            return str(ip), result.returncode == 0
        except:
            return str(ip), False

    def get(self, request, prefix_id):
        prefix = get_object_or_404(Prefix, id=prefix_id)
        messages.info(request, f"🔍 Starting status check for subnet {prefix.prefix}")

        try:
            online_tag = Tag.objects.get(slug='online')
        except Tag.DoesNotExist:
            online_tag = Tag.objects.create(name='online', slug='online')
            
        try:
            offline_tag = Tag.objects.get(slug='offline')
        except Tag.DoesNotExist:
            offline_tag = Tag.objects.create(name='offline', slug='offline')

        # Get only existing IPs in the subnet
        network = ip_network(prefix.prefix)
        all_ips = IPAddress.objects.filter(address__startswith=str(network.network_address).replace('.0', '.'))
        
        existing_ips = {}
        status_changes = []
        for ip in all_ips:
            ip_net = str(ip_interface(ip.address).ip)
            existing_ips[ip_net] = ip

        if not existing_ips:
            messages.warning(request, "No existing IPs found in this subnet")
            return redirect('ipam:prefix', pk=prefix_id)

        # Only ping IPs that exist in the database
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_ip = {executor.submit(self.ping_ip, ip_str): ip_str 
                          for ip_str in existing_ips.keys()}
            
            for future in concurrent.futures.as_completed(future_to_ip):
                ip_str, is_alive = future.result()
                ip_obj = existing_ips[ip_str]
                
                # Update IP status
                old_status = ip_obj.custom_field_data.get('Up_Down', None)
                ip_obj.custom_field_data['Up_Down'] = is_alive
                
                if is_alive:
                    ip_obj.tags.remove(offline_tag)
                    ip_obj.tags.add(online_tag)
                else:
                    ip_obj.tags.remove(online_tag)
                    ip_obj.tags.add(offline_tag)
                
                ip_obj.save()
                
                if old_status != is_alive:
                    status_changes.append(f"{ip_str}: {'🟢 up' if is_alive else '🔴 down'}")

        # Show summary message
        if status_changes:
            messages.success(request, f"✅ Status check complete - Changes detected:\n" + "\n".join(status_changes))
        else:
            messages.success(request, f"✅ Status check complete - No changes detected")

        return redirect('ipam:prefix', pk=prefix_id)

class ScanSubnetView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """View for scanning entire subnet and adding all discovered IPs"""
    permission_required = "ipam.view_prefix"

    def ping_ip(self, ip):
        """Ping a single IP address"""
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], 
                                  capture_output=True, 
                                  timeout=2)
            return str(ip), result.returncode == 0
        except:
            return str(ip), False

    def get(self, request, prefix_id):
        prefix = get_object_or_404(Prefix, id=prefix_id)
        messages.info(request, f"Initiating full scan of subnet {prefix.prefix}")

        prefix_length = prefix.prefix.prefixlen

        try:
            online_tag = Tag.objects.get(slug='online')
        except Tag.DoesNotExist:
            online_tag = Tag.objects.create(name='online', slug='online')
            
        try:
            offline_tag = Tag.objects.get(slug='offline')
        except Tag.DoesNotExist:
            offline_tag = Tag.objects.create(name='offline', slug='offline')

        network = ip_network(prefix.prefix)
        existing_ips = {str(ip_interface(ip.address).ip): ip 
                       for ip in IPAddress.objects.filter(address__net_contained=str(prefix.prefix))}
        
        discovered_ips = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            hosts = list(network.hosts()) if network.prefixlen < 31 else list(network)
            future_to_ip = {executor.submit(self.ping_ip, ip): ip for ip in hosts}
            
            for future in concurrent.futures.as_completed(future_to_ip):
                ip_str, is_alive = future.result()
                
                if is_alive:
                    if ip_str in existing_ips:
                        # Update existing IP
                        ip_obj = existing_ips[ip_str]
                        ip_obj.custom_field_data['Up_Down'] = True
                        ip_obj.tags.remove(offline_tag)
                        ip_obj.tags.add(online_tag)
                        ip_obj.save()
                        messages.info(request, f"Updated IP {ip_str} status to up")
                    else:
                        # Add new IP
                        discovered_ips.append(ip_str)
                        try:
                            ip_obj = IPAddress.objects.create(
                                address=f"{ip_str}/{prefix_length}",
                                status='active',
                                custom_field_data={'Up_Down': True}
                            )
                            ip_obj.tags.add(online_tag)
                            messages.success(request, f"Added new IP {ip_str}")
                        except Exception as e:
                            messages.error(request, f"Failed to add IP {ip_str}: {str(e)}")

        if discovered_ips:
            messages.success(request, f"Discovered {len(discovered_ips)} new IPs: {', '.join(discovered_ips)}")
        else:
            messages.info(request, "No new IPs discovered")

        return redirect('ipam:prefix', pk=prefix_id)