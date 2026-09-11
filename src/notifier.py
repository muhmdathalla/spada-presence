import os
import requests
import logging

logger = logging.getLogger("SpadaNotifier")

class TelegramNotifier:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.enabled = bool(self.bot_token and self.chat_id)
        if not self.enabled:
            logger.warning("Telegram notification is disabled: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not provided.")

    def send_message(self, message: str) -> bool:
        if not self.enabled:
            logger.info(f"[NOTIF LOCAL ONLY] {message}")
            return False
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            resp = requests.post(url, json=payload, timeout=15)
            if resp.status_code == 200:
                logger.info("Telegram message sent successfully.")
                return True
            else:
                logger.error(f"Failed to send Telegram message: {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False

    def send_photo(self, photo_path: str, caption: str = "") -> bool:
        if not self.enabled:
            logger.info(f"[NOTIF PHOTO LOCAL ONLY] Path: {photo_path} | Caption: {caption}")
            return False

        if not os.path.exists(photo_path):
            logger.warning(f"Screenshot file not found: {photo_path}, falling back to text message.")
            return self.send_message(caption)

        url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
        try:
            with open(photo_path, "rb") as photo_file:
                files = {"photo": photo_file}
                data = {
                    "chat_id": self.chat_id,
                    "caption": caption,
                    "parse_mode": "HTML"
                }
                resp = requests.post(url, files=files, data=data, timeout=30)
                if resp.status_code == 200:
                    logger.info("Telegram photo sent successfully.")
                    return True
                else:
                    logger.error(f"Failed to send Telegram photo: {resp.status_code} - {resp.text}")
                    # Fallback to text
                    return self.send_message(caption)
        except Exception as e:
            logger.error(f"Error sending Telegram photo: {e}")
            return self.send_message(caption)
