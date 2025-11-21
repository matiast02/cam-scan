# IP Scanner - Multi-Port Scanner for IP Cameras, DVR & NVR

Professional network scanning tool to identify IP cameras, DVRs, and NVRs with security vulnerabilities, especially those with default credentials.

## Features

- **Multi-Port Scanning**: Detects multiple services (RTSP, HTTP, ONVIF, proprietary protocols)
- **Automatic Identification**: Recognizes manufacturers (Hikvision, Dahua, Axis, etc.)
- **Credential Testing**: Verifies known default credentials
- **Parallel Scanning**: Uses multi-threading for fast scans
- **Detailed Reports**: Generates reports with ready-to-use URLs
- **Modular and Extensible**: Modular architecture for easy maintenance
- **Custom Credential Lists**: Support for loading custom username and password lists from text files

## Supported Protocols

- **RTSP** (554, 8554, 555, 7447)
- **HTTP/HTTPS** (80, 443, 8080, 8081, 8000, 9000, 5000)
- **ONVIF** (3702)
- **Dahua Proprietary** (37777, 37778)
- **Generic DVR** (34567, 6036, 7001)
- **RTMP** (1935)

## Project Structure

```
ip_scanner/
├── config/                 # Configurations
│   ├── __init__.py
│   ├── ports.py           # Port definitions
│   ├── credentials.py     # Credentials database
│   └── paths.py           # Common RTSP paths
├── protocols/             # Protocol handlers
│   ├── __init__.py
│   ├── http_handler.py    # HTTP/HTTPS
│   ├── rtsp_handler.py    # RTSP
│   ├── onvif_handler.py   # ONVIF
│   ├── dahua_handler.py   # Dahua proprietary
│   └── dvr_handler.py     # Generic DVR
├── scanner/               # Scanning logic
│   ├── __init__.py
│   ├── device_scanner.py  # Device scanning
│   ├── network_scanner.py # Network scanning
│   └── identifier.py      # Manufacturer identification
├── utils/                 # Utilities
│   ├── __init__.py
│   ├── network_utils.py   # Network functions
│   └── output_utils.py    # Output formatting
├── examples/              # Example files
│   ├── users.txt          # Example user list
│   └── passwords.txt      # Example password list
├── main.py               # Main script
└── README.md             # This file
```

## Installation

### Requirements

- Python 3.6 or higher
- Standard Python modules (no external dependencies required)

### Installation from source

```bash
# Clone or download the project
cd ip_scanner

# Optional: Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# No additional dependencies required
```

## Usage

### Basic Syntax

```bash
python3 main.py [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-n, --network` | Network to scan (e.g., 192.168.1.0/24) | Auto local network |
| `-p, --ports` | Specific ports separated by commas | All |
| `--preset` | Predefined preset (critical/rtsp/http/proprietary/all) | all |
| `-t, --timeout` | Scan timeout in seconds | 1 |
| `-a, --auth-timeout` | Authentication timeout in seconds | 3 |
| `-w, --workers` | Number of concurrent threads | 20 |
| `--userlist` | Text file with username list (one per line) | - |
| `--passlist` | Text file with password list (one per line) | - |

### Usage Examples

#### 1. Full Local Network Scan

```bash
python3 main.py
```

Automatically scans your local network with all configured ports.

#### 2. Quick Scan (Critical Ports Only)

```bash
python3 main.py --preset critical
```

Scans only the most important ports for faster results.

#### 3. RTSP Ports Only

```bash
python3 main.py --preset rtsp
```

Only searches for RTSP services.

#### 4. HTTP/Web Ports Only

```bash
python3 main.py --preset http
```

Only searches for web interfaces.

#### 5. Specific Ports

```bash
python3 main.py --ports 554,8554,37777,3702
```

Scans only the specified ports.

#### 6. Specific Network

```bash
python3 main.py -n 192.168.0.0/24
```

Scans a specific network instead of the local network.

#### 7. Fast Scan with More Threads

```bash
python3 main.py -n 192.168.0.0/24 -w 50 --preset critical
```

Uses 50 threads for faster scanning of critical ports.

#### 8. Detailed Scan with Long Timeouts

```bash
python3 main.py -t 2 -a 5
```

Increases timeouts for slow networks or slow-responding devices.

#### 9. Custom Username List

```bash
python3 main.py --preset critical --userlist users.txt
```

Uses a custom username list from a text file.

#### 10. Custom Password List

```bash
python3 main.py --preset critical --passlist passwords.txt
```

Uses a custom password list from a text file.

#### 11. Both Custom Lists

```bash
python3 main.py --preset critical --userlist users.txt --passlist passwords.txt
```

Uses both custom username and password lists.

## Available Presets

| Preset | Description | Ports |
|--------|-------------|-------|
| `critical` | Most important ports | 554, 8554, 8000, 37777, 34567, 80, 3702 |
| `rtsp` | RTSP only | 554, 8554, 555, 7447 |
| `http` | HTTP/HTTPS only | 80, 443, 8080, 8081, 8000, 9000, 5000 |
| `proprietary` | Proprietary protocols | 37777, 37778, 34567, 6036, 7001 |
| `all` | All ports | All configured ports |

## Custom Credential Lists

You can provide custom username and password lists via text files:

### Username List Format (`users.txt`)
```
# Comments start with #
# Empty lines are ignored

admin
root
user
default
```

### Password List Format (`passwords.txt`)
```
# One password per line

admin
12345
password
123456
```

The scanner will test all combinations of usernames × passwords. Example files are provided in the `examples/` directory.

## Example Output

```
================================================================================
  MULTI-PORT SCANNER FOR IP CAMERAS AND DVR
================================================================================
[*] Your local IP: 192.168.1.50
[*] Network to scan: 192.168.1.0/24
[*] Ports to scan: 17

[*] Scanning network: 192.168.1.0/24
[*] Ports to scan: 17
[*] Scan timeout: 1s | Auth: 3s
[*] Threads: 20
[*] Total IPs: 256
[*] Started: 2025-01-15 10:30:00

================================================================================
Ports:
    80 - HTTP       - Standard web
   554 - RTSP       - Standard RTSP
  3702 - ONVIF      - ONVIF Discovery
 37777 - DAHUA      - Dahua DVR/NVR
================================================================================

[+] 192.168.1.100    - Hikvision        - 4 port(s) - 3 accessible
[+] 192.168.1.101    - Dahua            - 3 port(s) - 2 accessible
[-] 192.168.1.102    - ONVIF Compatible - 2 port(s) - 0 accessible

[*] Scan completed in 45.23s

================================================================================
  SCAN SUMMARY
================================================================================
Total devices found: 3
VULNERABLE devices: 2
PROTECTED devices: 1

Distribution by manufacturer:
  - Hikvision: 1
  - Dahua: 1
  - ONVIF Compatible: 1

================================================================================
  [!] VULNERABLE DEVICES [!]
================================================================================

+-- 192.168.1.100 (camera-01.local)
+-- Manufacturer: Hikvision
+-- Accessible ports:
|
|  +-- Port 554 (RTSP)
|  +-- Description: Standard RTSP
|  +-- Server: RTSP Server
|  +-- Username: admin
|  +-- Password: 12345
|  +-- Suggested manufacturer: Hikvision
|  +-- URL: rtsp://admin:12345@192.168.1.100:554/Streaming/Channels/101
|      Path: /Streaming/Channels/101
+------------------------------------------------------------------------------
```

## Security and Responsible Use

⚠️ **IMPORTANT WARNING**:

This tool is designed for:
- Authorized security audits
- Testing on your own networks
- Identifying vulnerabilities in your own infrastructure
- Educational purposes

**DO NOT USE** for:
- Accessing networks without authorization
- Illegal or malicious activities
- Compromising the security of third-party systems

Misuse of this tool may be illegal in your jurisdiction.

## Security Recommendations

If you find vulnerable devices on your network:

1. **Change passwords immediately** - Use strong and unique passwords
2. **Disable unnecessary services** - Close unused ports
3. **Configure firewall** - Segment network and limit access
4. **Update firmware** - Keep devices up to date
5. **Disable Internet access** - Never expose cameras directly
6. **Use VPN** - For secure remote access
7. **Monitor access** - Review logs regularly

## Extending the Tool

### Add New Credentials

Edit `config/credentials.py`:

```python
DEFAULT_CREDENTIALS = [
    ("new_user", "new_password", "Manufacturer"),
    # ... more credentials
]
```

### Add New Ports

Edit `config/ports.py`:

```python
DEFAULT_PORTS = {
    9999: {'protocol': 'NEW', 'description': 'Description'},
    # ... more ports
}
```

### Add New RTSP Paths

Edit `config/paths.py`:

```python
RTSP_PATHS = [
    "/new/path",
    # ... more paths
]
```

### Create New Protocol Handler

1. Create a new file in `protocols/`
2. Implement the test function
3. Import in `protocols/__init__.py`
4. Use it in `scanner/device_scanner.py`

## Troubleshooting

### Error: "Could not detect local network"

- Verify your network connection
- Use `-n` to specify manually: `-n 192.168.1.0/24`

### Very Slow Scanning

- Reduce number of ports: `--preset critical`
- Increase threads: `-w 50`
- Reduce timeout: `-t 0.5 -a 2`

### Doesn't Find Known Devices

- Increase timeout: `-t 2 -a 5`
- Verify devices are on the correct network
- Some devices may not respond to certain ports

### Permission Errors on Linux

```bash
sudo python3 main.py
```

## Output Files

Results are automatically saved to:

```
scan_vulnerable_YYYYMMDD_HHMMSS.txt
```

Example: `scan_vulnerable_20250115_103045.txt`

## Contributing

To contribute to the project:

1. Add new protocols in `protocols/`
2. Add known credentials in `config/credentials.py`
3. Improve manufacturer detection in `scanner/identifier.py`
4. Report bugs and suggestions

## License

This project is for educational purposes and authorized security auditing only.

## Disclaimer

The author is not responsible for misuse of this tool. Use it only on networks and systems where you have express authorization.

---

**Last updated**: 2025-01-15
**Version**: 1.0.0
