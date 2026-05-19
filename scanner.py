import socket
import subprocess
import platform
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# =========================================
# COMMON PORTS
# =========================================

COMMON_PORTS = [
    21, 22, 23, 25,
    53, 80, 110,
    135, 139, 143,
    443, 445,
    3389, 8080
]

# =========================================
# PORT SERVICES
# =========================================

PORT_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "MSRPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP",
    8080: "HTTP-Alt"
}

# =========================================
# GET LOCAL IP
# =========================================

def get_local_ip():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:

        s.connect(("8.8.8.8", 80))

        ip = s.getsockname()[0]

    except:

        ip = "127.0.0.1"

    finally:

        s.close()

    return ip

# =========================================
# NETWORK RANGE
# =========================================

def get_network_range(local_ip):

    parts = local_ip.rsplit(".", 1)

    return parts[0] + ".0/24"

# =========================================
# PING DEVICE
# =========================================

def ping(ip):

    param = "-n" if platform.system().lower() == "windows" else "-c"

    command = [
        "ping",
        param,
        "1",
        str(ip)
    ]

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# =========================================
# GET MAC ADDRESS
# =========================================

def get_mac(ip):

    try:

        output = subprocess.check_output(
            "arp -a",
            shell=True,
            text=True
        )

        for line in output.splitlines():

            if ip in line:

                parts = line.split()

                for part in parts:

                    if "-" in part or ":" in part:
                        return part.upper()

    except:
        pass

    return "Unknown"

# =========================================
# HOSTNAME
# =========================================

def get_hostname(ip):

    try:
        return socket.gethostbyaddr(ip)[0]

    except:
        return "Unknown"

# =========================================
# PORT SCAN
# =========================================

def get_open_ports(ip):

    open_ports = []

    for port in COMMON_PORTS:

        try:

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(0.2)

            result = sock.connect_ex(
                (ip, port)
            )

            sock.close()

            if result == 0:

                open_ports.append(
                    PORT_SERVICES.get(
                        port,
                        str(port)
                    )
                )

        except:
            pass

    return open_ports

# =========================================
# DEVICE TYPE
# =========================================

def detect_device_type(hostname, services):

    hostname = hostname.lower()

    if "android" in hostname:
        return "Android Phone"

    if "iphone" in hostname:
        return "iPhone"

    if "tv" in hostname:
        return "Smart TV"

    if "camera" in hostname:
        return "CCTV Camera"

    if "printer" in hostname:
        return "Printer"

    if "SSH" in services:
        return "Linux Device"

    if "SMB" in services:
        return "Windows Device"

    if "HTTP" in services:
        return "Web Device"

    return "Unknown Device"

# =========================================
# SCAN HOST
# =========================================

def scan_host(ip):

    ping(ip)

    mac = get_mac(ip)

    if mac != "Unknown":

        hostname = get_hostname(ip)

        services = get_open_ports(ip)

        device_type = detect_device_type(
            hostname,
            services
        )

        return {
            "ip": ip,
            "mac": mac,
            "hostname": hostname,
            "device_type": device_type,
            "services": services
        }

    return None

# =========================================
# NETWORK SCAN
# =========================================

def scan_network():

    local_ip = get_local_ip()

    network_range = get_network_range(local_ip)

    print("\n" + "=" * 90)

    print("🔐 SIMPLE ADVANCED NETWORK SCANNER")

    print("=" * 90)

    print(f"Local IP : {local_ip}")

    print(f"Network  : {network_range}")

    print(f"Started  : {datetime.now()}")

    print("=" * 90)

    network = ipaddress.IPv4Network(
        network_range,
        strict=False
    )

    hosts = [
        str(ip)
        for ip in network.hosts()
    ]

    results = []

    with ThreadPoolExecutor(
        max_workers=200
    ) as executor:

        output = executor.map(
            scan_host,
            hosts
        )

    for result in output:

        if result:

            results.append(result)

            services = (
                ", ".join(result["services"])
                if result["services"]
                else "None"
            )

            print(
                f"✅ "
                f"{result['ip']:<16}"
                f"| "
                f"{result['mac']:<20}"
                f"| "
                f"{result['device_type']:<18}"
                f"| "
                f"{services}"
            )

    print("\n" + "=" * 90)

    print(f"Devices Found : {len(results)}")

    print("=" * 90)

    return results

# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    scan_network()

# =========================================
# IPV6 SUPPORT
# =========================================

def get_ipv6_addresses():

    ipv6_list = []

    try:

        hostname = socket.gethostname()

        addresses = socket.getaddrinfo(
            hostname,
            None,
            socket.AF_INET6
        )

        for addr in addresses:

            ip = addr[4][0]

            if "%" not in ip:

                ipv6_list.append(ip)

    except:
        pass

    return list(set(ipv6_list))