"""
HTTP/HTTPS protocol handler for camera and DVR web interfaces
"""

import http.client
import base64
import time


def test_http_auth(ip, port, username, password, timeout=3):
    """
    Test HTTP Basic Authentication

    Args:
        ip: Target IP address
        port: Target port
        username: Username to test
        password: Password to test
        timeout: Connection timeout in seconds

    Returns:
        tuple: (success, status_code, auth_type, server_info)
    """
    try:
        # Attempt HTTP/HTTPS connection
        if port == 443:
            conn = http.client.HTTPSConnection(str(ip), port, timeout=timeout)
        else:
            conn = http.client.HTTPConnection(str(ip), port, timeout=timeout)

        # First request without authentication
        conn.request("GET", "/")
        response = conn.getresponse()
        response.read()

        if response.status == 200:
            conn.close()
            return True, "200", "Sin autenticación", response.getheader('Server', 'Unknown')

        elif response.status == 401:
            conn.close()

            # Try with credentials if provided
            if username or password:
                time.sleep(0.1)

                if port == 443:
                    conn = http.client.HTTPSConnection(str(ip), port, timeout=timeout)
                else:
                    conn = http.client.HTTPConnection(str(ip), port, timeout=timeout)

                credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                headers = {"Authorization": f"Basic {credentials}"}

                conn.request("GET", "/", headers=headers)
                response = conn.getresponse()
                response.read()

                if response.status == 200:
                    conn.close()
                    return True, "200", "Basic Auth", response.getheader('Server', 'Unknown')

                conn.close()
                return False, "401", "Requiere auth", response.getheader('Server', 'Unknown')

            return False, "401", "Requiere auth", response.getheader('Server', 'Unknown')

        conn.close()
        return False, str(response.status), None, response.getheader('Server', 'Unknown')

    except Exception as e:
        return False, "Error", None, "Unknown"
