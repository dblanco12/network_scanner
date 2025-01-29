import socket
import ipaddress
import threading
import sys
from queue import Queue

# Define a worker function for threading
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is open on {ip}")
        sock.close()
    except socket.error:
        pass

# Function to scan a range of IP addresses
def scan_ips(start_ip, end_ip, ports):
    # Generate list of IPs to scan
    ip_range = [str(ip) for ip in ipaddress.IPv4Network(f"{start_ip}/24", strict=False).hosts()]
    print(f"Scanning IPs in range: {start_ip} - {end_ip}")

    # Create a queue for threads
    queue = Queue()

    # Create threads for each port scan
    def threaded_scan(ip):
        for port in ports:
            queue.put((ip, port))
    
    # Start scanning using threads
    def worker():
        while not queue.empty():
            ip, port = queue.get()
            scan_port(ip, port)
            queue.task_done()

    # Start scanning threads
    for ip in ip_range:
        threading.Thread(target=threaded_scan, args=(ip,)).start()

    # Wait for all threads to finish
    queue.join()

# Main function to handle user input and scan
def main():
    print("Network Scanner Tool")

    start_ip = input("Enter the start IP address (e.g., 192.168.1.1): ")
    end_ip = input("Enter the end IP address (e.g., 192.168.1.255): ")
    port_range = input("Enter the port range (e.g., 20-80): ")
    
    # Parse port range input
    port_start, port_end = map(int, port_range.split('-'))
    ports = list(range(port_start, port_end + 1))

    print(f"Scanning IP range: {start_ip} - {end_ip} for ports {port_start} to {port_end}")
    
    scan_ips(start_ip, end_ip, ports)

# Check if the script is being run directly
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit(0)
