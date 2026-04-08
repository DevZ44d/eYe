import psutil
import subprocess
import socket
import platform
import re, time
from collections import Counter
import urllib.request

class NetworkAnalyzer:
    def __init__(self):
        self.ssid = self._get_ssid()
        self.devices = self._discover_devices()
        self.network_details = self._analyze_network()

    def _run(self, cmd: str) -> str:
        try:
            output = subprocess.check_output(
                cmd,
                shell=True,
                text=True,
                stderr=subprocess.DEVNULL
            )
            return output
        except subprocess.CalledProcessError:
            return ""

    def _get_ssid(self):
        data = self._run("netsh wlan show interfaces")
        match = re.search(r"SSID\s*:\s*(.+)", data)
        if match:
            return match.group(1).strip()
        return None

    def config(self):
        if not self.ssid:
            return "No WiFi connection found"

        shell = self._run(
            f'ipconfig /all && netsh wlan show profile name="{self.ssid}" key=clear'
        )

        return shell

    def Password(self):
        try:
            shell = subprocess.check_output(
                f'''netsh wlan show profile name="{self.ssid}" key=clear''',
                shell=True,
                text=True
            )
            for Lines in shell.splitlines():
                if 'Key Content' in Lines:
                    Password = Lines.split(':')[1].strip()
                    return Password
                    break
            else:
                return "NoT Found Password"
        except subprocess.CalledProcessError as e:
            return e

    def _discover_devices(self):
        devices = {}
        ips = Counter()

        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED' and conn.raddr and conn.raddr.ip != '127.0.0.1':
                ips[conn.raddr.ip] += 1

        device_types = {
            443: "🌐 Web Server/Cloud",
            80: "🌍 HTTP Server",
            3389: "🖥️ RDP",
            22: "🔒 SSH Server",
            445: "📁 SMB/File Share",
            53: "🔍 DNS Server",
            3306: "🗄️ MySQL Server"
        }

        for ip, count in ips.most_common(10):
            ports = []

            for conn in psutil.net_connections(kind='inet'):
                if conn.raddr and conn.raddr.ip == ip:
                    ports.append(conn.raddr.port)

            device_type = "💻 Unknown Device"

            for port, dtype in device_types.items():
                if port in ports:
                    device_type = dtype
                    break

            devices[ip] = {
                "connections": count,
                "ports": sorted(set(ports))[:5],
                "type": device_type
            }

        return devices

    def get_service_name(self, port):
        try:
            return socket.getservbyport(port)
        except:
            return "unknown"

    def grab_banner(self, ip, port):

        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((ip, port))

            s.send(b"HEAD / HTTP/1.0\r\n\r\n")

            banner = s.recv(1024).decode(errors="ignore").strip()
            s.close()

            if banner:
                return banner.split("\n")[0][:60]

        except:
            pass

        return ""

    def open_ports(self):

        results = []
        localhost = "127.0.0.1"

        for conn in psutil.net_connections():

            if conn.status == "LISTEN":
                port = conn.laddr.port
                service = self.get_service_name(port)

                version = self.grab_banner(localhost, port)

                results.append({
                    "port": port,
                    "service": service,
                    "version": version
                })

        return sorted(results, key=lambda x: x["port"])

    def _analyze_network(self):

        details = []
        details.append("SYSTEM")

        details.append(f"Python: {platform.python_version()}")

        uptime_seconds = int(time.time() - psutil.boot_time())
        uptime_hours = uptime_seconds // 3600

        details.append(f"Uptime: {uptime_hours} hours")

        details.append("\nNETWORK")
        hostname = socket.gethostname()
        details.append(f"Hostname: {hostname}")
        details.append(f"SSID: {self.ssid} , Password : {self.Password()}")
        try:
            public_ip = urllib.request.urlopen("https://api.ipify.org").read().decode()
        except:
            public_ip = "Unknown"

        details.append(f"Public IP: {public_ip}")
        dns = re.findall(r"DNS Servers[^\:]*:\s*([\d\.]+)", self._run("ipconfig /all"))
        if dns:
            details.append(f"DNS: {dns[0]}")

        details.append("\nINTERFACES")
        stats = psutil.net_if_stats()
        for nic, addrs in psutil.net_if_addrs().items():
            ip = None
            mac = None
            for addr in addrs:

                if addr.family == socket.AF_INET:
                    ip = addr.address

                if addr.family == psutil.AF_LINK:
                    mac = addr.address

            if ip:
                speed = stats[nic].speed if nic in stats else "N/A"

                details.append(
                    f"{nic} | IP: {ip} | MAC: {mac} | Speed: {speed} Mbps"
                )


        net = psutil.net_io_counters()
        details.append("\nTRAFFIC")
        details.append(f"Bytes Sent: {net.bytes_sent}")
        details.append(f"Bytes Received: {net.bytes_recv}")

        ports = self.open_ports()
        details.append("\nOPEN PORTS")

        if ports:
            details.append(", ".join(map(str, ports)))
        details.append("\nDISCOVERED DEVICES")

        for i, (ip, info) in enumerate(self.devices.items(), 1):
            ports_str = ", ".join(map(str, info["ports"]))
            details.append(
                f"{i}. {ip} | {info['type']} | {info['connections']} conns | Ports: {ports_str}"
            )

        return details

    def save_to_file(self, filename="network_report.txt"):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("🕵️ NETWORK INTELLIGENCE REPORT\n")
            f.write("=" * 50 + "\n\n")

            for line in self.network_details:
                f.write(line + "\n")

            f.write("\n" + "=" * 50 + "\n")
            f.write("\nWiFi CONFIGURATION\n")
            f.write("-" * 50 + "\n")
            f.write(self.config())
            f.write("\nOPEN PORTS\n")
            f.write("PORT     STATE SERVICE        VERSION\n")

            for p in self.open_ports():
                port = str(p["port"]).ljust(8)
                service = p["service"].ljust(13)
                version = p["version"]

                f.write(f"{port} open  {service} {version}\n")

        return filename
