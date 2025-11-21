# Usage Guide - IP Scanner

## Common Use Cases

### 1. First Security Audit on Corporate Network

**Scenario**: You need to audit camera security in an office.

```bash
# Step 1: Quick initial scan
python3 main.py --preset critical

# Step 2: If you find devices, full scan
python3 main.py

# Step 3: Document and report
# Results are automatically saved in scan_vulnerable_*.txt
```

### 2. RTSP-Specific Audit

**Scenario**: You're only interested in cameras with exposed RTSP.

```bash
python3 main.py --preset rtsp -w 30
```

### 3. Large Network (> 1000 devices)

**Scenario**: Scan a large enterprise network.

```bash
# Use more threads and short timeout
python3 main.py -n 10.0.0.0/22 -w 100 -t 0.5 -a 2 --preset critical
```

### 4. Slow or Wireless Network

**Scenario**: Devices with slow response.

```bash
# Increase timeouts
python3 main.py -t 3 -a 10 -w 10
```

### 5. Find Only Web Interfaces

**Scenario**: Identify all camera web interfaces.

```bash
python3 main.py --preset http
```

### 6. Multiple Networks

**Scenario**: Audit multiple subnets.

```bash
# Scan each network separately
python3 main.py -n 192.168.1.0/24
python3 main.py -n 192.168.2.0/24
python3 main.py -n 192.168.3.0/24
```

### 7. Post-Hardening Verification

**Scenario**: Verify security measures are working.

```bash
# Before hardening - document
python3 main.py > before.txt

# After changing passwords and closing ports
python3 main.py > after.txt

# Compare results
diff before.txt after.txt
```

### 8. Custom Credential Testing

**Scenario**: Test organization-specific credentials.

```bash
# Use custom username list
python3 main.py --userlist company_users.txt

# Use custom password list
python3 main.py --passlist company_passwords.txt

# Use both
python3 main.py --userlist users.txt --passlist passwords.txt
```

## Result Interpretation

### Symbols

- `[+]` **Vulnerable**: Device with accessible ports (VULNERABLE)
- `[-]` **Protected**: Device detected but protected

### Information Displayed

```
[+] 192.168.1.100    - Hikvision        - 4 port(s) - 3 accessible
    └─ IP            └─ Manufacturer    └─ Total     └─ Vulnerable
```

### Severity Levels

| Accessible Ports | Severity | Required Action |
|-----------------|----------|-----------------|
| 0 | ✅ Secure | Verify configuration |
| 1-2 | ⚠️ Medium | Change passwords |
| 3+ | 🚨 High | Immediate action |

## Understanding the Output

### Real-time Output

During scan:
```
[*] Scanning network: 192.168.1.0/24
[*] Ports to scan: 17
[*] Scan timeout: 1s | Auth: 3s
[*] Threads: 20

[+] 192.168.1.100    - Hikvision        - 4 port(s) - 3 accessible
[*] Progress: 25/254 IPs scanned
```

### Final Report

After scan:
```
================================================================================
  SCAN SUMMARY
================================================================================
Total devices found: 5
VULNERABLE devices: 3
PROTECTED devices: 2

Distribution by manufacturer:
  - Hikvision: 2
  - Dahua: 1
  - ONVIF Compatible: 2
```

### Detailed Vulnerable Device Info

```
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

## Custom Credential Lists

### Format

**users.txt** (one username per line):
```
admin
root
user
operator
# Comments start with #
default
```

**passwords.txt** (one password per line):
```
admin
12345
password
# Empty passwords supported
123456
company2024
```

### Usage

```bash
# Test all combinations (5 users × 5 passwords = 25 combinations)
python3 main.py --userlist users.txt --passlist passwords.txt --preset critical
```

### Best Practices

1. **Start small**: Test with a few credentials first
2. **Be specific**: Use organization-specific defaults
3. **Document**: Keep track of which lists you've tested
4. **Secure files**: Protect credential list files appropriately

## Advanced Usage

### Combining Options

```bash
# Fast scan of specific network with custom credentials
python3 main.py -n 192.168.0.0/24 \
                --preset critical \
                -w 50 \
                -t 0.5 \
                -a 2 \
                --userlist users.txt \
                --passlist passwords.txt
```

### Targeted Port Scanning

```bash
# Only scan specific ports
python3 main.py --ports 554,80,8000,37777
```

### Multiple Scans

```bash
# Script for multiple networks
for net in 192.168.{1..10}.0/24; do
  python3 main.py -n $net --preset critical
done
```

## Performance Tuning

### Fast Scan (Large Networks)

```bash
python3 main.py -w 100 -t 0.3 -a 1 --preset critical
```

**Pros**: Very fast
**Cons**: May miss slow devices

### Thorough Scan (Complete Coverage)

```bash
python3 main.py -w 10 -t 3 -a 10
```

**Pros**: Finds all devices
**Cons**: Very slow

### Balanced Scan (Recommended)

```bash
python3 main.py -w 30 -t 1 -a 3 --preset critical
```

**Pros**: Good balance
**Cons**: None

## Output Files

### Automatic Saving

Results are automatically saved to:
```
scan_vulnerable_YYYYMMDD_HHMMSS.txt
```

### File Contents

- Complete list of vulnerable devices
- Credentials found
- URLs ready to use
- Manufacturer information

### Using Output Files

```bash
# View results
cat scan_vulnerable_*.txt

# Extract RTSP URLs
grep "rtsp://" scan_vulnerable_*.txt

# Count vulnerable devices
grep -c "Username:" scan_vulnerable_*.txt
```

## Security Best Practices

### After Finding Vulnerabilities

1. **Immediate Action**:
   - Change all default passwords
   - Use strong, unique passwords
   - Document all changes

2. **Network Segmentation**:
   - Isolate cameras from main network
   - Use VLANs for camera traffic
   - Implement firewall rules

3. **Access Control**:
   - Disable unnecessary ports
   - Restrict access by IP
   - Use VPN for remote access

4. **Monitoring**:
   - Enable logging
   - Monitor access patterns
   - Set up alerts

5. **Maintenance**:
   - Regular firmware updates
   - Periodic security audits
   - Review access logs

## Troubleshooting

### No Devices Found

**Possible causes**:
- Wrong network range
- Devices are actually secure
- Network connectivity issues

**Solutions**:
```bash
# Verify network
ip addr  # Linux/macOS
ipconfig  # Windows

# Test with longer timeout
python3 main.py -t 3 -a 10

# Test specific IP
python3 main.py -n 192.168.1.100/32
```

### Very Slow Scanning

**Possible causes**:
- Too many threads
- Network congestion
- Slow devices

**Solutions**:
```bash
# Reduce threads
python3 main.py -w 10

# Reduce timeout
python3 main.py -t 0.5 -a 2

# Use critical preset only
python3 main.py --preset critical
```

### Permission Errors

**Linux/macOS**:
```bash
sudo python3 main.py
```

**Windows**:
Run terminal as Administrator

## FAQ

**Q: Can I scan the Internet?**
A: Not recommended. Designed for local/internal networks.

**Q: Works on Windows/Mac/Linux?**
A: Yes, it's cross-platform (standard Python).

**Q: Requires root/admin permissions?**
A: No for ports > 1024. Some systems may require it.

**Q: Saves found passwords?**
A: Yes, in scan_vulnerable_*.txt file (protect appropriately!).

**Q: Affects the devices?**
A: No, read-only. Doesn't modify configurations.

**Q: Detects all devices?**
A: Detects those responding to known protocols. Some very old or exotic devices may not be detected.

**Q: How many credentials does it test by default?**
A: Default list has ~50 common credentials. Custom lists can have unlimited entries.

**Q: Can I stop and resume a scan?**
A: No, scans run to completion. Use Ctrl+C to stop.

---

For more information, see the main README.md
