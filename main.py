#!/usr/bin/env python3
"""
IP Scanner - Multi-port scanner for IP cameras, DVR, and NVR systems

Main entry point for the application
"""

import argparse
from datetime import datetime

from config import DEFAULT_PORTS
from config.ports import PORT_PRESETS
from utils import get_local_network, display_results
from scanner import scan_network


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Escáner multi-puerto para cámaras IP, DVR y NVR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s                              # Escaneo completo de red local
  %(prog)s -n 192.168.1.0/24           # Red específica
  %(prog)s --ports 554,8554,80,37777   # Puertos específicos
  %(prog)s --preset rtsp               # Solo puertos RTSP
  %(prog)s --preset critical           # Solo puertos críticos
  %(prog)s --preset all                # Todos los puertos
        """
    )

    parser.add_argument('-n', '--network', help='Red a escanear (ej: 192.168.1.0/24)')
    parser.add_argument('-p', '--ports', help='Puertos específicos separados por comas')
    parser.add_argument('--preset',
                       choices=['critical', 'rtsp', 'http', 'proprietary', 'all'],
                       help='Preset de puertos predefinido')
    parser.add_argument('-t', '--timeout', type=float, default=1,
                       help='Timeout escaneo (default: 1)')
    parser.add_argument('-a', '--auth-timeout', type=float, default=3,
                       help='Timeout autenticación (default: 3)')
    parser.add_argument('-w', '--workers', type=int, default=20,
                       help='Hilos concurrentes (default: 20)')

    return parser.parse_args()


def determine_network(args):
    """
    Determine network range to scan

    Args:
        args: Parsed command line arguments

    Returns:
        tuple: (network_range, local_ip)
    """
    if args.network:
        return args.network, "Manual"
    else:
        network_range, local_ip = get_local_network()
        if not network_range:
            print("[!] No se pudo detectar la red local")
            return None, None
        return network_range, local_ip


def determine_ports(args):
    """
    Determine which ports to scan

    Args:
        args: Parsed command line arguments

    Returns:
        dict: Dictionary of ports to scan
    """
    if args.ports:
        # Custom ports
        custom_ports = {}
        for port_str in args.ports.split(','):
            try:
                port = int(port_str.strip())
                if port in DEFAULT_PORTS:
                    custom_ports[port] = DEFAULT_PORTS[port]
                else:
                    custom_ports[port] = {'protocol': 'UNKNOWN', 'description': 'Puerto personalizado'}
            except:
                pass
        return custom_ports

    elif args.preset:
        # Use preset
        if args.preset == 'all':
            return DEFAULT_PORTS
        else:
            port_list = PORT_PRESETS.get(args.preset, [])
            return {port: DEFAULT_PORTS[port] for port in port_list if port in DEFAULT_PORTS}

    else:
        # All default ports
        return DEFAULT_PORTS


def main():
    """Main application entry point"""
    args = parse_arguments()

    # Determine network
    network_range, local_ip = determine_network(args)
    if not network_range:
        return

    # Determine ports to scan
    ports_to_scan = determine_ports(args)

    print("=" * 80)
    print("  ESCÁNER MULTI-PUERTO PARA CÁMARAS IP Y DVR")
    print("=" * 80)
    print(f"[*] Tu IP local: {local_ip}")
    print(f"[*] Red a escanear: {network_range}")
    print(f"[*] Puertos a escanear: {len(ports_to_scan)}")

    # Scan network
    start_time = datetime.now()
    devices = scan_network(
        network_range,
        ports_to_scan,
        args.timeout,
        args.auth_timeout,
        args.workers
    )
    end_time = datetime.now()

    print(f"\n[*] Escaneo completado en {(end_time - start_time).total_seconds():.2f}s")

    # Display results
    display_results(devices)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Escaneo interrumpido")
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
