"""
Network utility functions for scanning and discovery
"""

import socket
import ipaddress


def get_local_network():
    """
    Automatically detect the local network

    Returns:
        tuple: (network_range, local_ip) or (None, None) if detection fails
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
        return str(network), local_ip
    except Exception as e:
        return None, None


def scan_port(ip, port, timeout=1):
    """
    Scan a specific port to check if it's open

    Args:
        ip: Target IP address
        port: Port to scan
        timeout: Connection timeout in seconds

    Returns:
        bool: True if port is open, False otherwise
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((str(ip), port))
        sock.close()
        return result == 0
    except:
        return False


def get_hostname(ip):
    """
    Get hostname for an IP address

    Args:
        ip: IP address to lookup

    Returns:
        str: Hostname or "Unknown" if lookup fails
    """
    try:
        return socket.gethostbyaddr(str(ip))[0]
    except:
        return "Unknown"
