"""
Generic Chinese DVR protocol handler
"""

import socket


def test_generic_dvr(ip, port=34567, timeout=3):
    """
    Test generic Chinese DVR protocol

    Args:
        ip: Target IP address
        port: Target port (default 34567)
        timeout: Connection timeout in seconds

    Returns:
        tuple: (success, status, details)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((str(ip), port))

        # Basic handshake common in Chinese DVRs
        handshake = b'\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        sock.sendall(handshake)
        response = sock.recv(1024)
        sock.close()

        if len(response) > 0:
            return True, "DVR Genérico", "Puerto activo"

        return False, "No responde", None

    except:
        return False, "Error", None
