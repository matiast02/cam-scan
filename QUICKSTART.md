# Quick Start - IP Scanner

## 5-Minute Getting Started Guide

### 1. Run Your First Scan (Auto-detect local network)

```bash
cd ip_scanner
python3 main.py --preset critical
```

This will:
- Auto-detect your local network
- Scan the most critical ports (554, 8000, 37777, etc.)
- Show results in real-time
- Save vulnerable devices to a text file

### 2. Scan a Specific Network

```bash
python3 main.py -n 192.168.1.0/24
```

### 3. Faster Scan (More threads)

```bash
python3 main.py --preset critical -w 50
```

### 4. Only RTSP Cameras

```bash
python3 main.py --preset rtsp
```

### 5. Only Web Interfaces

```bash
python3 main.py --preset http
```

## Understanding Output

```
🟢 192.168.1.100    - Hikvision        - 4 puerto(s) - 3 accesible(s)
```

- 🟢 = Device with accessible services (vulnerable)
- 🔵 = Device found but protected
- IP: 192.168.1.100
- Manufacturer: Hikvision
- 4 ports open, 3 accessible with default credentials

## Common Use Cases

### Home Network Audit
```bash
python3 main.py --preset critical
```

### Office Network Audit
```bash
python3 main.py -n 10.0.0.0/24 -w 30
```

### Find All RTSP Streams
```bash
python3 main.py --preset rtsp
cat scan_vulnerable_*.txt | grep "rtsp://"
```

### Quick Check (Very Fast)
```bash
python3 main.py --preset critical -t 0.5 -a 1 -w 100
```

### Thorough Scan (Slow but Complete)
```bash
python3 main.py -t 3 -a 10 -w 10
```

## Next Steps

1. **Read results**: `cat scan_vulnerable_*.txt`
2. **Secure devices**: Change default passwords
3. **Learn more**: Read `README.md` and `USAGE.md`
4. **Customize**: Edit `config/` files
5. **Extend**: Add your own code in `examples/`

## All Options

```
-n, --network         Network to scan (e.g., 192.168.1.0/24)
-p, --ports           Specific ports (e.g., 554,8000,37777)
--preset              Preset: critical/rtsp/http/proprietary/all
-t, --timeout         Scan timeout in seconds (default: 1)
-a, --auth-timeout    Auth timeout in seconds (default: 3)
-w, --workers         Number of threads (default: 20)
```

## Presets

| Preset | Ports | Use Case |
|--------|-------|----------|
| critical | 7 most important | Fast general scan |
| rtsp | RTSP only | Find cameras |
| http | Web only | Find web interfaces |
| proprietary | Dahua/DVR | Find Chinese DVRs |
| all | All configured | Complete scan |

## Tips

- Start with `--preset critical` (fastest)
- Use `-w 50` or more for large networks
- Use `-t 0.5 -a 2` for slow networks
- Results are saved automatically

## Help

```bash
python3 main.py --help
```

For detailed documentation, see:
- `README.md` - Overview
- `USAGE.md` - Detailed guide
- `INSTALL.md` - Installation
- `PROJECT_STRUCTURE.md` - Architecture

---

**Happy scanning! Remember: Only scan networks you own or have permission to audit.**
