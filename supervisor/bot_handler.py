from __future__ import annotations

from typing import Dict, Any, Optional
import os
import logging

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
        self.owner_token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not self.support_token:
            raise ValueError("TELEGRAM_BOT_TOKEN_ARCHITECT env variable is missing")
            
        if not self.owner_token:
            raise ValueError("TELEGRAM_BOT_TOKEN env variable is missing")
            
        self.log = logging.getLogger(__name__)

    def route_message(self, message: Dict[str, Any]) -> str:
        """
        Returns the bot context: 'owner' or 'support'
        """
        if not message:
            self.log.warning("Empty message received")
            return 'support'
            
        chat_data = message.get('chat')
        if not chat_data:
            self.log.warning("Message missing 'chat' data")
            return 'support'
            
        chat_id = chat_data.get('id')
        if chat_id is None:
            self.log.warning("Message chat data missing 'id'")
            return 'support'
        
        if chat_id == self.owner_id:
            return 'owner'
        
        # All other chats go to support bot
        return 'support'

    def get_active_tokens(self) -> Dict[str, str]:
        """
        Returns available bot tokens
        """
        return {
            'owner': self.owner_token,
            'support': self.support_token
        }