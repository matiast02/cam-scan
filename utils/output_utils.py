"""
Output formatting and result display utilities
"""

from datetime import datetime


def display_results(devices):
    """
    Display detailed scan results

    Args:
        devices: List of device dictionaries with scan results
    """
    from scanner.identifier import identify_manufacturer

    if not devices:
        print("\n[!] No se encontraron dispositivos")
        return

    # Separate by accessibility
    vulnerable = [d for d in devices if any(p['accessible'] for p in d['ports'])]
    secured = [d for d in devices if d not in vulnerable]

    print("\n" + "=" * 80)
    print(f"  RESUMEN DEL ESCANEO")
    print("=" * 80)
    print(f"Total dispositivos encontrados: {len(devices)}")
    print(f"Dispositivos VULNERABLES: {len(vulnerable)}")
    print(f"Dispositivos PROTEGIDOS: {len(secured)}")

    # Statistics by manufacturer
    manufacturers = {}
    for device in devices:
        mfr = identify_manufacturer(device)
        manufacturers[mfr] = manufacturers.get(mfr, 0) + 1

    print(f"\nDistribución por fabricante:")
    for mfr, count in sorted(manufacturers.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {mfr}: {count}")

    # Display vulnerable devices
    if vulnerable:
        print("\n" + "=" * 80)
        print("  [!] DISPOSITIVOS VULNERABLES [!]")
        print("=" * 80)

        for device in vulnerable:
            print(f"\n+-- {device['ip']} ({device['hostname']})")
            print(f"+-- Fabricante: {identify_manufacturer(device)}")
            print(f"+-- Puertos accesibles:")

            for port_info in device['ports']:
                if port_info['accessible']:
                    print(f"|")
                    print(f"|  +-- Puerto {port_info['port']} ({port_info['protocol']})")
                    print(f"|  +-- Descripcion: {port_info['description']}")
                    print(f"|  +-- Servidor: {port_info['server']}")

                    if port_info.get('credentials'):
                        creds = port_info['credentials']
                        print(f"|  +-- Usuario: {creds['username'] if creds['username'] else '(vacio)'}")
                        print(f"|  +-- Password: {creds['password'] if creds['password'] else '(vacio)'}")
                        print(f"|  +-- Fabricante sugerido: {creds['manufacturer']}")

                    if port_info.get('details'):
                        if isinstance(port_info['details'], dict):
                            if 'url' in port_info['details']:
                                print(f"|  +-- URL: {port_info['details']['url']}")
                            if 'path' in port_info['details']:
                                print(f"|      Path: {port_info['details']['path']}")
                        else:
                            print(f"|  +-- Info: {port_info['details']}")

            print(f"+{'-' * 78}")

    # Display protected devices (summary)
    if secured:
        print("\n" + "=" * 80)
        print("  [#] DISPOSITIVOS PROTEGIDOS")
        print("=" * 80)

        for device in secured:
            ports_list = ", ".join([f"{p['port']}({p['protocol']})" for p in device['ports']])
            print(f"  {device['ip']:15} - {identify_manufacturer(device):15} - Puertos: {ports_list}")

    # Save results
    if vulnerable:
        _save_results_to_file(vulnerable)

    # Security warning
    if vulnerable:
        _display_security_warning()


def _save_results_to_file(vulnerable_devices):
    """
    Save vulnerable devices to a text file

    Args:
        vulnerable_devices: List of vulnerable device dictionaries
    """
    from scanner.identifier import identify_manufacturer

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"scan_vulnerable_{timestamp}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("DISPOSITIVOS VULNERABLES - ESCANEO MULTI-PUERTO\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        for device in vulnerable_devices:
            f.write(f"IP: {device['ip']}\n")
            f.write(f"Hostname: {device['hostname']}\n")
            f.write(f"Fabricante: {identify_manufacturer(device)}\n\n")

            for port_info in device['ports']:
                if port_info['accessible']:
                    f.write(f"  Puerto {port_info['port']} - {port_info['protocol']}\n")
                    if port_info.get('credentials'):
                        f.write(f"    Usuario: {port_info['credentials']['username']}\n")
                        f.write(f"    Password: {port_info['credentials']['password']}\n")
                    if port_info.get('details') and isinstance(port_info['details'], dict):
                        if 'url' in port_info['details']:
                            f.write(f"    URL: {port_info['details']['url']}\n")
                    f.write("\n")

            f.write("-" * 80 + "\n\n")

    print(f"\n[+] Resultados guardados en: {filename}")


def _display_security_warning():
    """Display critical security warning"""
    print("\n" + "[!] " * 20)
    print("\n  ADVERTENCIA CRITICA DE SEGURIDAD")
    print("\n  Los dispositivos listados tienen servicios accesibles con credenciales")
    print("  por defecto y representan un RIESGO DE SEGURIDAD GRAVE.")
    print("\n  RECOMENDACIONES URGENTES:")
    print("  1. Cambiar TODAS las contrasenas inmediatamente")
    print("  2. Deshabilitar servicios innecesarios")
    print("  3. Configurar firewall/segmentacion de red")
    print("  4. Actualizar firmware")
    print("  5. Deshabilitar acceso desde Internet")
    print("\n" + "[!] " * 20 + "\n")


def print_scan_header(network_range, local_ip, ports_to_scan, timeout_scan, timeout_auth, max_workers):
    """
    Print scan header information

    Args:
        network_range: Network range being scanned
        local_ip: Local IP address
        ports_to_scan: Dictionary of ports to scan
        timeout_scan: Scan timeout
        timeout_auth: Authentication timeout
        max_workers: Number of worker threads
    """
    import ipaddress

    network = ipaddress.IPv4Network(network_range)

    print("\n[*] Escaneando red: {}".format(network_range))
    print(f"[*] Puertos a escanear: {len(ports_to_scan)}")
    print(f"[*] Timeout escaneo: {timeout_scan}s | Auth: {timeout_auth}s")
    print(f"[*] Hilos: {max_workers}")
    print(f"[*] Total IPs: {network.num_addresses}")
    print(f"[*] Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 80)

    # Display ports to scan
    print("Puertos:")
    for port, info in sorted(ports_to_scan.items()):
        print(f"  {port:5} - {info['protocol']:10} - {info['description']}")
    print("=" * 80 + "\n")


def print_device_found(device_ip, manufacturer, total_ports, accessible_ports):
    """
    Print information about a found device

    Args:
        device_ip: Device IP address
        manufacturer: Identified manufacturer
        total_ports: Total number of open ports
        accessible_ports: Number of accessible ports
    """
    status = "[+]" if accessible_ports > 0 else "[-]"
    print(f"{status} {device_ip:15} - {manufacturer:15} - "
          f"{total_ports} puerto(s) - {accessible_ports} accesible(s)")


def print_progress(completed, total):
    """
    Print scan progress

    Args:
        completed: Number of IPs scanned
        total: Total IPs to scan
    """
    print(f"[*] Progreso: {completed}/{total} IPs escaneadas")
