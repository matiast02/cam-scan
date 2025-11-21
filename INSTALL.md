# Installation Guide - IP Scanner

## Quick Installation

### Linux / macOS

```bash
# 1. Download or clone the project
cd /path/to/ip_scanner

# 2. Make executable
chmod +x main.py

# 3. Run
python3 main.py --help
```

### Windows

```cmd
# 1. Navigate to directory
cd C:\path\to\ip_scanner

# 2. Run
python main.py --help
```

## Package Installation

### Development Mode Installation

```bash
cd ip_scanner
pip install -e .
```

After this, you can run from anywhere:
```bash
ip-scanner --help
```

### Standard Installation

```bash
cd ip_scanner
pip install .
```

## Verify Installation

```bash
# Verify Python
python3 --version
# Must be >= 3.6

# Verify modules
python3 -c "import socket, ipaddress, concurrent.futures; print('OK')"
```

## Installation on Different Systems

### Ubuntu / Debian

```bash
# Python already installed, verify version
python3 --version

# If you need to install Python 3
sudo apt update
sudo apt install python3 python3-pip

# Clone/download project
cd ip_scanner

# Run
python3 main.py
```

### CentOS / RHEL / Fedora

```bash
# Verify or install Python 3
sudo dnf install python3

# Clone/download project
cd ip_scanner

# Run
python3 main.py
```

### macOS

```bash
# Python 3 comes with modern macOS
python3 --version

# If not installed, install with Homebrew
brew install python3

# Clone/download project
cd ip_scanner

# Run
python3 main.py
```

### Windows

**Option 1: Microsoft Store**
```
1. Open Microsoft Store
2. Search "Python 3"
3. Install Python 3.x
```

**Option 2: python.org**
```
1. Download from https://python.org
2. Run installer
3. Check "Add Python to PATH"
```

Then:
```cmd
cd ip_scanner
python main.py --help
```

## Docker (Optional)

```bash
# Build image
docker build -t ip-scanner .

# Run
docker run -it --network host ip-scanner --preset critical
```

## Troubleshooting

### "python3 command not found"
```bash
# Try python instead of python3
python --version

# Or install Python 3
# Ubuntu/Debian: sudo apt install python3
# macOS: brew install python3
```

### Permission Errors (Linux/macOS)
```bash
# Run with sudo for privileged ports
sudo python3 main.py
```

### Import Errors
```bash
# Verify you're in the correct directory
pwd
ls main.py  # Should exist

# Verify Python path
python3 -c "import sys; print(sys.path)"
```

## Recommended Initial Configuration

After installing, test with:

```bash
# 1. Quick test scan
python3 main.py --preset critical -t 0.5 -w 10

# 2. If it works, full scan
python3 main.py

# 3. Check results
ls -lh scan_*.txt
```

## Uninstallation

```bash
# If installed as package
pip uninstall ip-scanner

# If running from source, just delete the directory
rm -rf /path/to/ip_scanner
```

---

For more information, see README.md and USAGE.md
