#!/usr/bin/env python3
"""
Example: Custom scanning script using IP Scanner modules

This example shows how to use IP Scanner modules programmatically
to create custom scanning workflows.
"""

import sys
import os

# Add parent directory to path to import ip_scanner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ip_scanner.config import DEFAULT_PORTS
from ip_scanner.scanner import scan_device
from ip_scanner.utils import get_local_network
from ip_scanner.scanner.identifier import identify_manufacturer


def scan_specific_ip(ip_address):
    """
    Example: Scan a specific IP address
    """
    print(f"Scanning {ip_address}...")

    # Define which ports to scan
    ports = {
        554: DEFAULT_PORTS[554],
        80: DEFAULT_PORTS[80],
        8000: DEFAULT_PORTS[8000],
    }

    # Scan the device
    result = scan_device(ip_address, ports, timeout_scan=1, timeout_auth=3)

    if result:
        print(f"\nDevice found: {result['ip']}")
        print(f"Hostname: {result['hostname']}")
        print(f"Manufacturer: {identify_manufacturer(result)}")
        print(f"\nOpen ports:")
        for port_info in result['ports']:
            print(f"  - Port {port_info['port']}: {port_info['protocol']}")
            if port_info['accessible']:
                print(f"    ACCESSIBLE with: {port_info['credentials']}")
    else:
        print(f"No open ports found on {ip_address}")


def scan_ip_range(start_ip, end_ip):
    """
    Example: Scan a range of IP addresses
    """
    import ipaddress

    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)

    current = start
    while current <= end:
        scan_specific_ip(str(current))
        current += 1


def find_hikvision_cameras():
    """
    Example: Find only Hikvision cameras
    """
    network, local_ip = get_local_network()
    if not network:
        print("Could not detect local network")
        return

    print(f"Searching for Hikvision cameras on {network}...")

    # Hikvision typically uses these ports
    hikvision_ports = {
        8000: DEFAULT_PORTS[8000],
        554: DEFAULT_PORTS[554],
        80: DEFAULT_PORTS[80],
    }

    import ipaddress
    from concurrent.futures import ThreadPoolExecutor

    net = ipaddress.IPv4Network(network)

    def check_ip(ip):
        result = scan_device(ip, hikvision_ports, timeout_scan=1, timeout_auth=2)
        if result:
            mfr = identify_manufacturer(result)
            if 'hikvision' in mfr.lower():
                return result
        return None

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(check_ip, net.hosts())

    hikvision_devices = [r for r in results if r]

    print(f"\nFound {len(hikvision_devices)} Hikvision camera(s)")
    for device in hikvision_devices:
        print(f"  - {device['ip']}: {len(device['ports'])} port(s)")


def export_to_json():
    """
    Example: Export scan results to JSON
    """
    import json
    from ip_scanner.scanner import scan_network
    from ip_scanner.config import DEFAULT_PORTS

    network, _ = get_local_network()
    if not network:
        return

    # Scan with critical ports only
    critical_ports = {
        554: DEFAULT_PORTS[554],
        80: DEFAULT_PORTS[80],
        8000: DEFAULT_PORTS[8000],
    }

    print(f"Scanning {network}...")
    devices = scan_network(network, critical_ports, timeout_scan=1, timeout_auth=2, max_workers=20)

    # Convert to JSON-serializable format
    output = []
    for device in devices:
        output.append({
            'ip': device['ip'],
            'hostname': device['hostname'],
            'manufacturer': identify_manufacturer(device),
            'ports': device['ports']
        })

    # Save to JSON file
    with open('scan_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to scan_results.json")


if __name__ == "__main__":
    print("IP Scanner - Custom Examples\n")
    print("1. Scan specific IP")
    print("2. Scan IP range")
    print("3. Find Hikvision cameras")
    print("4. Export to JSON")

    choice = input("\nSelect example (1-4): ").strip()

    if choice == "1":
        ip = input("Enter IP address: ").strip()
        scan_specific_ip(ip)

    elif choice == "2":
        start = input("Enter start IP: ").strip()
        end = input("Enter end IP: ").strip()
        scan_ip_range(start, end)

    elif choice == "3":
        find_hikvision_cameras()

    elif choice == "4":
        export_to_json()

    else:
        print("Invalid choice")
