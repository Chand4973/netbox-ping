import re
from typing import Iterable
from dataclasses import dataclass
import dns.resolver
import socket
import logging

logger = logging.getLogger('netbox.netbox_ping')

def split(s):
    for x, y in re.findall(r'(\d*)(\D*)', s):
        yield '', int(x or '0')
        yield y, 0


def natural_keys(c):

    return tuple(split(c))


def human_sorted(iterable: Iterable):
    return sorted(iterable, key=natural_keys)


@dataclass(frozen=True)
class UnifiedInterface:
    """A unified way to represent the interface and interface template"""
    id: int
    name: str
    type: str
    type_display: str
    mgmt_only: bool = False
    is_template: bool = False

    def __eq__(self, other):
        # Ignore some fields when comparing; ignore interface name case and whitespaces
        return (self.name.lower().replace(' ', '') == other.name.lower().replace(' ', '')) and (self.type == other.type)

    def __hash__(self):
        # Ignore some fields when hashing; ignore interface name case and whitespaces
        return hash((self.name.lower().replace(' ', ''), self.type))


def perform_dns_lookup(ip, dns_servers=None):
    """
    Perform forward and reverse DNS lookups
    Returns tuple of (hostname, status)
    """
    logger.info(f"Attempting DNS lookup for IP: {ip}")
    if dns_servers:
        logger.info(f"Using DNS servers: {dns_servers}")
    
    try:
        # Configure resolver with custom DNS servers if provided
        resolver = dns.resolver.Resolver()
        if dns_servers:
            resolver.nameservers = [server for server in dns_servers if server]
            logger.debug(f"Configured resolver with nameservers: {resolver.nameservers}")

        # Try reverse DNS lookup
        logger.debug(f"Attempting reverse DNS lookup for {ip}")
        hostname = socket.gethostbyaddr(ip)[0]
        logger.info(f"Reverse DNS lookup successful: {ip} -> {hostname}")
        
        # Try forward DNS lookup to verify
        logger.debug(f"Attempting forward DNS lookup for {hostname}")
        forward_ips = resolver.resolve(hostname, 'A')
        
        # Check if the IP matches any of the forward lookup results
        if any(str(rdata) == ip for rdata in forward_ips):
            logger.info(f"Forward DNS lookup verified: {hostname} -> {ip}")
            return hostname, True
        
        logger.warning(f"Forward DNS lookup did not match original IP: {hostname} -> {[str(ip) for ip in forward_ips]}")
        return hostname, False
    except socket.herror as e:
        logger.warning(f"Reverse DNS lookup failed for {ip}: {str(e)}")
        return None, False
    except dns.resolver.NXDOMAIN:
        logger.warning(f"Forward DNS lookup failed - domain not found for {hostname}")
        return None, False
    except Exception as e:
        logger.error(f"DNS lookup failed for {ip}: {str(e)}")
        return None, False