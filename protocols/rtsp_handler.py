"""
RTSP protocol handler for camera streams
"""

import socket
import base64
import time


def test_rtsp_auth(ip, port, username, password, path="/", timeout=3):
    """
    Test RTSP authentication

    Args:
        ip: Target IP address
        port: Target port
        username: Username to test
        password: Password to test
        path: RTSP path to test
        timeout: Connection timeout in seconds

    Returns:
        tuple: (success, status_code, auth_type, server_info)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((str(ip), port))

        full_url = f"rtsp://{ip}:{port}{path}"

        rtsp_request = f"OPTIONS {full_url} RTSP/1.0\r\n"
        rtsp_request += "CSeq: 1\r\n"
        rtsp_request += "User-Agent: Python Scanner\r\n\r\n"

        sock.sendall(rtsp_request.encode())
        response = sock.recv(4096).decode('utf-8', errors='ignore')

        server_info = "Unknown"
        if "Server:" in response:
            server_line = [line for line in response.split('\n') if 'Server:' in line]
            if server_line:
                server_info = server_line[0].replace("Server:", "").strip()

        if "200 OK" in response:
            sock.close()
            return True, "200", "Sin auth", server_info

        elif "401" in response:
            sock.close()

            if username or password:
                time.sleep(0.1)

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                sock.connect((str(ip), port))

                credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

                rtsp_request = f"OPTIONS {full_url} RTSP/1.0\r\n"
                rtsp_request += "CSeq: 2\r\n"
                rtsp_request += f"Authorization: Basic {credentials}\r\n"
                rtsp_request += "User-Agent: Python Scanner\r\n\r\n"

                sock.sendall(rtsp_request.encode())
                response2 = sock.recv(4096).decode('utf-8', errors='ignore')
                sock.close()

                if "200 OK" in response2:
                    return True, "200", "Basic Auth", server_info

            return False, "401", "Requiere auth", server_info

        sock.close()
        return False, "404", None, server_info

    except:
        return False, "Error", None, "Unknown"
