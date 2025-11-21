"""
Device scanning functionality
"""

from utils.network_utils import scan_port, get_hostname
from protocols import (
    test_http_auth,
    test_rtsp_auth,
    test_onvif_discovery,
    test_dahua_protocol,
    test_generic_dvr
)
from config import DEFAULT_CREDENTIALS, RTSP_PATHS


def scan_single_port(ip, port, port_info, timeout_scan=1, timeout_auth=3, custom_credentials=None):
    """
    Scan a specific port and identify the service

    Args:
        ip: Target IP address
        port: Port to scan
        port_info: Port information dictionary
        timeout_scan: Scan timeout
        timeout_auth: Authentication timeout
        custom_credentials: Optional list of custom credentials to test

    Returns:
        dict: Port scan result or None if port is closed
    """
    if not scan_port(ip, port, timeout_scan):
        return None

    protocol = port_info['protocol']
    result = {
        'port': port,
        'protocol': protocol,
        'description': port_info['description'],
        'status': 'open',
        'accessible': False,
        'credentials': None,
        'server': 'Unknown',
        'details': None
    }

    # Test based on protocol
    if protocol == 'RTSP':
        result = _test_rtsp_port(ip, port, result, timeout_auth, custom_credentials)

    elif protocol in ['HTTP', 'HTTPS']:
        result = _test_http_port(ip, port, result, timeout_auth, custom_credentials)

    elif protocol == 'ONVIF':
        result = _test_onvif_port(ip, result, timeout_auth)

    elif protocol == 'DAHUA':
        result = _test_dahua_port(ip, port, result, timeout_auth)

    elif protocol == 'DVR':
        result = _test_dvr_port(ip, port, result, timeout_auth)

    return result


def _test_rtsp_port(ip, port, result, timeout, custom_credentials=None):
    """Test RTSP port with common paths and credentials"""
    # Use custom credentials if provided, otherwise use defaults
    credentials_to_test = custom_credentials if custom_credentials else DEFAULT_CREDENTIALS[:10]

    # Test common RTSP paths
    for path in RTSP_PATHS[:5]:  # Test first 5 paths
        for username, password, mfr in credentials_to_test:
            success, status, auth_type, server = test_rtsp_auth(
                ip, port, username, password, path, timeout
            )

            if success:
                result['accessible'] = True
                result['credentials'] = {
                    'username': username,
                    'password': password,
                    'manufacturer': mfr
                }
                result['server'] = server
                result['details'] = {
                    'path': path,
                    'auth_type': auth_type,
                    'url': f"rtsp://{username}:{password}@{ip}:{port}{path}" if username else f"rtsp://{ip}:{port}{path}"
                }
                return result

    result['server'] = 'RTSP Server'
    result['details'] = 'Protegido o rutas no encontradas'
    return result


def _test_http_port(ip, port, result, timeout, custom_credentials=None):
    """Test HTTP/HTTPS port with credentials"""
    # Use custom credentials if provided, otherwise use defaults
    credentials_to_test = custom_credentials if custom_credentials else DEFAULT_CREDENTIALS[:10]

    for username, password, mfr in credentials_to_test:
        success, status, auth_type, server = test_http_auth(
            ip, port, username, password, timeout
        )

        if success:
            result['accessible'] = True
            result['credentials'] = {
                'username': username,
                'password': password,
                'manufacturer': mfr
            }
            result['server'] = server
            result['details'] = {
                'auth_type': auth_type,
                'url': f"http{'s' if port == 443 else ''}://{ip}:{port}/"
            }
            return result

    # At least identify the web server
    _, _, _, server = test_http_auth(ip, port, "", "", timeout)
    result['server'] = server
    result['details'] = 'Interfaz web disponible (protegida)'
    return result


def _test_onvif_port(ip, result, timeout):
    """Test ONVIF discovery"""
    success, status, details = test_onvif_discovery(ip, timeout)
    if success:
        result['accessible'] = True
        result['server'] = 'ONVIF'
        result['details'] = details
    else:
        result['details'] = status
    return result


def _test_dahua_port(ip, port, result, timeout):
    """Test Dahua proprietary protocol"""
    success, status, details = test_dahua_protocol(ip, port, timeout=timeout)
    if success:
        result['server'] = status
        result['details'] = details
        # Try Dahua credentials
        result['details'] = 'Puerto Dahua activo (probar credenciales manualmente)'
    else:
        result['details'] = status
    return result


def _test_dvr_port(ip, port, result, timeout):
    """Test generic DVR protocol"""
    success, status, details = test_generic_dvr(ip, port, timeout=timeout)
    if success:
        result['server'] = status
        result['details'] = details
    else:
        result['details'] = status
    return result


def scan_device(ip, ports_to_scan, timeout_scan=1, timeout_auth=3, custom_credentials=None):
    """
    Scan all ports of a device

    Args:
        ip: Target IP address
        ports_to_scan: Dictionary of ports to scan
        timeout_scan: Scan timeout
        timeout_auth: Authentication timeout
        custom_credentials: Optional list of custom credentials to test

    Returns:
        dict: Device information or None if no ports are open
    """
    hostname = get_hostname(ip)

    device_info = {
        'ip': str(ip),
        'hostname': hostname,
        'ports': []
    }

    for port, port_info in ports_to_scan.items():
        result = scan_single_port(ip, port, port_info, timeout_scan, timeout_auth, custom_credentials)
        if result:
            device_info['ports'].append(result)

    if device_info['ports']:
        return device_info

    return None
