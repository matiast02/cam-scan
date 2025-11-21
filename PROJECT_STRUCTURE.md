# IP Scanner Project Structure

## Overview

```
ip_scanner/
├── config/                    # Configuration modules
│   ├── __init__.py           # Export main configurations
│   ├── ports.py              # Port definitions and presets
│   ├── credentials.py        # Default credentials database
│   └── paths.py              # Common RTSP paths by manufacturer
│
├── protocols/                 # Protocol handlers
│   ├── __init__.py           # Export all handlers
│   ├── http_handler.py       # HTTP/HTTPS handler
│   ├── rtsp_handler.py       # RTSP handler
│   ├── onvif_handler.py      # ONVIF discovery handler
│   ├── dahua_handler.py      # Dahua proprietary protocol
│   └── dvr_handler.py        # Generic DVR protocol
│
├── scanner/                   # Scanning logic
│   ├── __init__.py           # Export scanning functions
│   ├── device_scanner.py     # Individual device scanning
│   ├── network_scanner.py    # Full network scanning
│   └── identifier.py         # Manufacturer identification
│
├── utils/                     # Utilities
│   ├── __init__.py           # Export utilities
│   ├── network_utils.py      # Network functions (scan_port, get_hostname, etc.)
│   └── output_utils.py       # Result formatting and presentation
│
├── examples/                  # Usage examples
│   ├── custom_scan.py        # Custom scan scripts
│   ├── users.txt             # Example username list
│   └── passwords.txt         # Example password list
│
├── __init__.py               # Package initialization
├── main.py                   # Main entry point
├── setup.py                  # Installation configuration
├── requirements.txt          # Dependencies (none external)
├── .gitignore               # Files to ignore in git
├── LICENSE                   # MIT License
├── README.md                # Main documentation
├── QUICKSTART.md            # Quick start guide
├── USAGE.md                 # Detailed usage guide
├── INSTALL.md               # Installation guide
└── PROJECT_STRUCTURE.md     # This file
```

## Module Descriptions

### 1. Config (config/)

**Purpose**: Centralize all scanner configurations.

- **ports.py**: Defines all ports to scan and their characteristics
  - `DEFAULT_PORTS`: Dictionary with ports and metadata
  - `PORT_PRESETS`: Predefined presets (critical, rtsp, http, etc.)

- **credentials.py**: Known credentials database
  - `DEFAULT_CREDENTIALS`: List of tuples (user, pass, manufacturer)

- **paths.py**: Common RTSP paths
  - `RTSP_PATHS`: List of common paths
  - `RTSP_PATHS_BY_MANUFACTURER`: Manufacturer-specific paths

### 2. Protocols (protocols/)

**Purpose**: Implement protocol-specific logic.

Each handler follows the same pattern:
```python
def test_PROTOCOL(ip, port, username, password, timeout=3):
    """
    Returns: (success, status, details)
    """
```

- **http_handler.py**: Tests HTTP Basic authentication
- **rtsp_handler.py**: Tests RTSP authentication
- **onvif_handler.py**: WS-Discovery
- **dahua_handler.py**: Dahua binary protocol
- **dvr_handler.py**: Generic Chinese DVR protocol

### 3. Scanner (scanner/)

**Purpose**: Coordinate device and network scanning.

- **device_scanner.py**:
  - `scan_single_port()`: Scans a specific port
  - `scan_device()`: Scans all ports of a device
  - Internal `_test_*_port()` functions for each protocol type

- **network_scanner.py**:
  - `scan_network()`: Scans entire network using ThreadPoolExecutor
  - Coordinates parallel scanning of multiple devices

- **identifier.py**:
  - `identify_manufacturer()`: Identifies manufacturer based on services

### 4. Utils (utils/)

**Purpose**: Reusable utility functions.

- **network_utils.py**:
  - `get_local_network()`: Auto-detect local network
  - `scan_port()`: TCP port scan
  - `get_hostname()`: Reverse DNS lookup

- **output_utils.py**:
  - `display_results()`: Format and display results
  - `print_scan_header()`: Print scan configuration
  - `print_device_found()`: Print found device
  - `print_progress()`: Print scan progress

### 5. Main (main.py)

**Purpose**: Application entry point.

Functions:
- `parse_arguments()`: Parse command-line arguments
- `determine_network()`: Determine network to scan
- `determine_ports()`: Determine ports to scan
- `load_custom_credentials()`: Load custom credential lists
- `main()`: Main execution flow

## Data Flow

### Scan Execution Flow

```
main.py
  ├─> parse_arguments()
  ├─> determine_network()
  ├─> determine_ports()
  ├─> load_custom_credentials()  [NEW]
  └─> scan_network()
       └─> ThreadPoolExecutor
            └─> scan_device() (parallel for each IP)
                 └─> scan_single_port() (for each port)
                      ├─> scan_port() (TCP connection test)
                      └─> test_*_protocol() (credential testing)
                           └─> Protocol-specific handlers
```

### Credential Testing Flow

```
Custom Lists (optional)
  ↓
load_custom_credentials()
  ↓
Create combinations (users × passwords)
  ↓
Pass to scan_network()
  ↓
Used by scan_device()
  ↓
Tested by protocol handlers
```

## Architecture Patterns

### Modular Design

Each component is independent and can be modified without affecting others:
- **Config**: Change ports/credentials without touching code
- **Protocols**: Add new protocols by creating new handler
- **Scanner**: Modify scan logic independently
- **Utils**: Shared utilities used across modules

### Extensibility

Easy to extend:
1. **New Protocol**: Create `protocols/new_handler.py`
2. **New Credential Source**: Modify `load_custom_credentials()`
3. **New Port Preset**: Add to `config/ports.py`
4. **New Output Format**: Modify `utils/output_utils.py`

### Error Handling

- Graceful degradation (failures don't stop scan)
- Timeouts prevent hanging
- Exceptions caught and logged

## Key Design Decisions

### 1. No External Dependencies

- Uses only Python standard library
- Easy installation and deployment
- No version conflicts

### 2. Multi-threading

- Uses `concurrent.futures.ThreadPoolExecutor`
- Configurable thread count
- Scales well for large networks

### 3. Protocol Abstraction

- Each protocol in separate handler
- Consistent return format
- Easy to add new protocols

### 4. Configuration-Driven

- Ports defined in configuration
- Credentials in separate file
- Easy customization without code changes

### 5. Custom Credential Support

- Load from external text files
- Comment support in files
- Unlimited credential combinations
- Falls back to defaults if not provided

## File Relationships

### Import Chain

```
main.py
  ├─> config
  │    ├─> ports.py
  │    ├─> credentials.py
  │    └─> paths.py
  ├─> scanner
  │    ├─> network_scanner.py
  │    │    └─> device_scanner.py
  │    │         ├─> protocols/*
  │    │         └─> utils/network_utils.py
  │    └─> identifier.py
  └─> utils
       ├─> network_utils.py
       └─> output_utils.py
```

### Data Flow

```
User Input (CLI)
     ↓
main.py (orchestration)
     ↓
scanner/ (execution)
     ↓
protocols/ (testing)
     ↓
utils/ (helpers)
     ↓
Output (screen + file)
```

## Adding Features

### Example: Add New Protocol

1. Create `protocols/new_protocol_handler.py`:
```python
def test_new_protocol(ip, port, username, password, timeout=3):
    # Implementation
    return (success, status, details)
```

2. Import in `protocols/__init__.py`:
```python
from protocols.new_protocol_handler import test_new_protocol
```

3. Use in `scanner/device_scanner.py`:
```python
elif protocol == 'NEW_PROTOCOL':
    result = _test_new_protocol_port(ip, port, result, timeout)
```

### Example: Add New Port Preset

Edit `config/ports.py`:
```python
PORT_PRESETS = {
    'my_preset': [80, 554, 8000],  # Your ports
    # ... existing presets
}
```

### Example: Add Custom Credential Source

Modify `main.py`:
```python
def load_custom_credentials(args):
    # Add new source (e.g., database, API)
    if args.credential_db:
        return load_from_database(args.credential_db)
    # ... existing logic
```

## Testing Strategy

### Manual Testing

```bash
# Test specific components
python3 -c "from scanner import scan_device; print(scan_device.__doc__)"

# Test configuration
python3 -c "from config import DEFAULT_PORTS; print(len(DEFAULT_PORTS))"

# Test protocol handler
python3 -c "from protocols import test_http_auth; print(test_http_auth.__doc__)"
```

### Integration Testing

```bash
# Small network test
python3 main.py -n 192.168.1.0/29 --preset critical

# Custom credential test
python3 main.py -n 192.168.1.0/29 --userlist examples/users.txt
```

## Performance Considerations

### Thread Count

- Default: 20 threads
- Large networks: 50-100 threads
- Slow networks: 10-20 threads

### Timeouts

- Scan timeout: 1s (default)
- Auth timeout: 3s (default)
- Adjust based on network speed

### Memory Usage

- Low memory footprint
- Results stored per-device
- Scales to thousands of devices

## Security Considerations

### Credential Storage

- Default credentials in code (read-only)
- Custom credentials in text files (user-provided)
- Output files contain passwords (protect appropriately)

### Network Impact

- Read-only scanning
- No modification of devices
- Minimal network traffic

### Responsible Use

- Only scan authorized networks
- Document all scans
- Secure scan results

---

For more details, see README.md and other documentation files.
