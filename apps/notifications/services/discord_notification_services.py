import requests
from django.conf import settings

class DiscordNotificationService:
    BASE_URL = settings.BASE_DISCORD_URL

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
    
    def send_message(self, channel_id: str, content: str) -> bool:
        url = f"{self.BASE_URL}/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "content": content
        }
        response = requests
        response = response.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
        
    def notify_schedule_conflict(self, channel_id, user_discord_id, notification_message):
        discord_ids = ', '.join([f"<@{uid}>" for uid in user_discord_id])
        content = f"{discord_ids} \n {notification_message}"
        self.send_message(channel_id=channel_id, content=content)