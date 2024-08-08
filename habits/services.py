import requests

from config import settings


def send_notification(text, chat_id):
    params = {"text": text, "chat_id": chat_id}
    response = requests.post(
        f"{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
        params=params,
    )
    response.raise_for_status()
