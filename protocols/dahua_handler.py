"""
Dahua proprietary protocol handler
"""

import socket


def test_dahua_protocol(ip, port=37777, username="admin", password="admin", timeout=3):
    """
    Test Dahua proprietary protocol

    Args:
        ip: Target IP address
        port: Target port (default 37777)
        username: Username to test
        password: Password to test
        timeout: Connection timeout in seconds

    Returns:
        tuple: (success, status, details)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((str(ip), port))

        # Basic Dahua login (simplified)
        # The actual protocol is more complex but this identifies the service
        login_packet = b'\xa0\x00\x00\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        sock.sendall(login_packet)
        response = sock.recv(1024)
        sock.close()

        if len(response) > 0:
            # If it responds, it's probably Dahua
            if response[0:2] == b'\xb0\x00' or response[0:2] == b'\xa1\x00':
                return True, "Dahua DVR/NVR", "Protocolo propietario activo"

        return False, "No responde", None

    except:
        return False, "Error", None
