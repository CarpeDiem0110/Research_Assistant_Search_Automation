
import requests


TELEGRAM_BOT_TOKEN = "7796630658:AAGQWYsg_1TEK1Mpy30gzqBxPFeDGhNPw6s"
TELEGRAM_CHAT_ID = "5219479758"

class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                print("❌ Telegram message failed:", response.text)
            else:
                print("📤 Telegram message sent successfully.")
        except Exception as e:
            print("❌ Error sending Telegram message:", str(e))