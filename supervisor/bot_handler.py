import os
from typing import Dict, Any

class BotHandler:
    """
    Handles routing between multiple Telegram bots:
    - Main bot (owner/development)
    - Support bot (architects)
    """

    def __init__(self, state_manager):
        self.state = state_manager
        self.owner_id = state_manager.get('owner_id')
        self.support_token = os.getenv('TELEGRAM_BOT_TOKEN_ARCHITECT')
        
        if not self.support_token:
            raise ValueError("TELEGRAM_BOT_TOKEN_ARCHITECT env variable is missing")

    def route_message(self, message: Dict[str, Any]) -> str:
        """
        Returns the bot context: 'owner' or 'support'
        """
        chat_id = message.get('chat', {}).get('id')
        
        if chat_id == self.owner_id:
            return 'owner'
        
        # All other chats go to support bot
        return 'support'

    def get_active_tokens(self) -> Dict[str, str]:
        """
        Returns available bot tokens
        """
        return {
            'owner': os.getenv('TELEGRAM_BOT_TOKEN'),
            'support': self.support_token
        }