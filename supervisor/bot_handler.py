from __future__ import annotations

from typing import Dict, Any, Optional
import os
import logging

# Import feedback manager
from feedback_manager import UserFeedbackManager

class BotHandler:
    """
    Handles routing between multiple Telegram bots and collects user feedback:
    - Main bot (owner/development) 
    - Support bot (architects) with integrated feedback collection
    
    TEMPORARILY DISABLED FOR DEBUGGING
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
            
        # Initialize feedback manager
        # DISABLED FOR DEBUGGING
        # self.feedback_manager = UserFeedbackManager()
        # self.feedback_context = {}  # Tracks which users need to provide comments
        
        self.log = logging.getLogger(__name__)

    def route_message(self, message: Dict[str, Any]) -> str:
        """
        Returns the bot context: 'owner' or 'support'
        """
        # TEMPORARILY ROUTING ALL TO OWNER FOR DEBUGGING
        return 'owner'

    def get_active_tokens(self) -> Dict[str, str]:
        """
        Returns available bot tokens
        """
        # Return only owner token for now
        return {
            'owner': self.owner_token
            # 'support': self.support_token  # DISABLED
        }
    
    def should_request_feedback(self, chat_id: int) -> bool:
        """
        Check if feedback should be requested for this chat
        """
        return False  # DISABLED FOR DEBUGGING
    
    def handle_feedback_request(self, chat_id: int, response_message_id: int) -> str:
        """
        Send feedback request after a support response
        """
        return ""  # DISABLED
    
    def handle_feedback_submission(self, chat_id: int, message_text: str) -> str:
        """
        Handle user's feedback submission (rating or comment)
        """
        return ""  # DISABLED
    
    def _parse_rating(self, text: str) -> Optional[int]:
        """
        Parse rating from text (1-5)
        """
        return None  # DISABLED
    
    def _now_iso(self) -> str:
        """
        Get current time in ISO format
        """
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()