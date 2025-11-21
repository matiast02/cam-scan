"""
Network-wide scanning functionality
"""

import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from scanner.device_scanner import scan_device
from scanner.identifier import identify_manufacturer
from utils.output_utils import print_scan_header, print_device_found, print_progress


def scan_network(network_range, ports_to_scan, timeout_scan=1, timeout_auth=3, max_workers=20, custom_credentials=None):
    """
    Scan entire network for devices

    Args:
        network_range: Network range to scan (e.g., '192.168.1.0/24')
        ports_to_scan: Dictionary of ports to scan
        timeout_scan: Scan timeout
        timeout_auth: Authentication timeout
        max_workers: Number of concurrent threads
        custom_credentials: Optional list of custom credentials to test

    Returns:
        list: List of found devices
    """
    network = ipaddress.IPv4Network(network_range)
    devices_found = []

    print_scan_header(network_range, "Auto", ports_to_scan, timeout_scan, timeout_auth, max_workers)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {
            executor.submit(scan_device, ip, ports_to_scan, timeout_scan, timeout_auth, custom_credentials): ip
            for ip in network.hosts()
        }

        completed = 0
        for future in as_completed(future_to_ip):
            completed += 1
            device = future.result()

            if completed % 25 == 0:
                print_progress(completed, network.num_addresses - 2)

            if device and device['ports']:
                devices_found.append(device)

                # Identify manufacturer
                manufacturer = identify_manufacturer(device)

                # Count open and accessible ports
                total_ports = len(device['ports'])
                accessible_ports = sum(1 for p in device['ports'] if p['accessible'])

                print_device_found(device['ip'], manufacturer, total_ports, accessible_ports)

    return devices_found
