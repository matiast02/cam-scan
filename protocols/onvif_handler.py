"""
ONVIF protocol handler for discovery and device identification
"""

import socket
import xml.etree.ElementTree as ET


def test_onvif_discovery(ip, timeout=3):
    """
    Attempt ONVIF discovery using WS-Discovery

    Args:
        ip: Target IP address
        timeout: Connection timeout in seconds

    Returns:
        tuple: (success, status, details)
    """
    try:
        # WS-Discovery message for ONVIF
        probe_msg = '''<?xml version="1.0" encoding="UTF-8"?>
<e:Envelope xmlns:e="http://www.w3.org/2003/05/soap-envelope"
            xmlns:w="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:d="http://schemas.xmlsoap.org/ws/2005/04/discovery"
            xmlns:dn="http://www.onvif.org/ver10/network/wsdl">
    <e:Header>
        <w:MessageID>uuid:84ede3de-7dec-11d0-c360-F01234567890</w:MessageID>
        <w:To>urn:schemas-xmlsoap-org:ws:2005:04:discovery</w:To>
        <w:Action>http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</w:Action>
    </e:Header>
    <e:Body>
        <d:Probe>
            <d:Types>dn:NetworkVideoTransmitter</d:Types>
        </d:Probe>
    </e:Body>
</e:Envelope>'''

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)

        # Send probe to port 3702
        sock.sendto(probe_msg.encode(), (str(ip), 3702))

        try:
            data, addr = sock.recvfrom(8192)
            sock.close()

            # Parse XML response
            response = data.decode('utf-8', errors='ignore')
            if 'onvif' in response.lower() or 'NetworkVideoTransmitter' in response:
                # Extract basic information
                try:
                    root = ET.fromstring(response)
                    # Look for XAddrs (service addresses)
                    namespaces = {
                        'd': 'http://schemas.xmlsoap.org/ws/2005/04/discovery'
                    }
                    xaddrs = root.find('.//d:XAddrs', namespaces)
                    if xaddrs is not None and xaddrs.text:
                        return True, "ONVIF Compatible", xaddrs.text.split()[0]
                except:
                    pass

                return True, "ONVIF Compatible", "Dispositivo encontrado"
        except socket.timeout:
            sock.close()
            return False, "No responde", None

    except Exception as e:
        return False, "Error", None

    return False, "No ONVIF", None
