# Network Scanner - Feature Additions and Implementation Guide

This document outlines potential feature enhancements for the network scanner and provides step-by-step instructions for implementation.

---

## 🚀 Planned Features

### 1. **Service Detection**
   - Identify which service is running on an open port.
   - Example: If port 80 is open, display "HTTP Server Detected."

### 2. **OS Fingerprinting**
   - Estimate the target device's operating system based on responses.
   - Requires `scapy` or `python-nmap`.

### 3. **Live Host Discovary (Ping Sweep)**
   - Identify active devices in the network before scanning for ports.
   - Reduce scanning time by skipping inactive host.

### 4. **Save Scan Results to a File**
   - Store results in a text or JSON file for later review.

### 5. **Multi-threaded Scanning Optimization**
   - Improve performance by optimizing threading

### 6. **Nmap Integration**
   - Use `nmap` (if instaled) to enhance scanning features.

---

## 🛠 How to Implement Each Feature

### 1️⃣ **Service Detection**
#### Steps:
1. Modify `scan_port()` to attempt retrieving the service name.
2. Use Python’s `socket.getservbyport(port)` to check known services.
3. Display the service name next to open ports.

#### Example Code:
```python
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "Unknown Service"
            print(f"Port {port} is open on {ip} ({service})")
        sock.close()
    except socket.error:
        pass
