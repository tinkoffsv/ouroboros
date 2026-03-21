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
        self.feedback_manager = UserFeedbackManager()
        self.feedback_context = {}  # Tracks which users need to provide comments
        
        self.log = logging.getLogger(__name__)

    def route_message(self, message: Dict[str, Any]) -> str:
        """
        Returns the bot context: 'owner' or 'support'
        """
        # Get chat ID
        chat_id = message['chat']['id']
        
        # If this is a feedback comment from a user who previously gave low rating
        if chat_id in self.feedback_context:
            return 'support'
            
        # Owner gets special routing
        if chat_id == self.owner_id:
            return 'owner'

        # All other chats are support
        return 'support'

    def get_active_tokens(self) -> Dict[str, str]:
        """
        Returns available bot tokens
        """
        return {
            'owner': self.owner_token,
            'support': self.support_token
        }
    
    def should_request_feedback(self, chat_id: int) -> bool:
        """
        Check if feedback should be requested for this chat
        """
        # Never request feedback from owner
        if chat_id == self.owner_id:
            return False
            
        # Don't request feedback when user is providing comment
        if chat_id in self.feedback_context:
            return False
            
        # Request feedback for all support interactions
        return True
    
    def handle_feedback_request(self, chat_id: int, response_message_id: int) -> str:
        """
        Send feedback request after a support response
        """
        # Store that this user should provide feedback
        self.feedback_context[chat_id] = {
            'response_message_id': response_message_id,
            'timestamp': self._now_iso()
        }
        
        return "Оцените ответ по шкале от 1 до 5 звёзд: 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣\n(1-3 — плохой, 4-5 — хороший)"
    
    def handle_feedback_submission(self, chat_id: int, message_text: str) -> str:
        """
        Handle user's feedback submission (rating or comment)
        """
        if chat_id not in self.feedback_context:
            return ""

        rating = self._parse_rating(message_text)
        
        if rating is not None:
            # Clear feedback context
            response_msg_id = self.feedback_context[chat_id]['response_message_id']
            del self.feedback_context[chat_id]
            
            # Save feedback
            self.feedback_manager.save_feedback(
                user_id=chat_id,
                message_id=response_msg_id,
                rating=rating
            )
            
            # Ask for comment if rating is low
            if rating <= 3:
                self.feedback_context[chat_id] = {
                    'rating': rating,
                    'response_message_id': response_msg_id,
                    'expecting_comment': True,
                    'timestamp': self._now_iso()
                }
                return "Спасибо за оценку. Пожалуйста, кратко опишите, что можно улучшить?"
            else:
                return "Спасибо за высокую оценку! 🙏"
        
        # Check if expecting a comment
        if (chat_id in self.feedback_context and 
            self.feedback_context[chat_id].get('expecting_comment')):
            
            rating = self.feedback_context[chat_id]['rating']
            response_msg_id = self.feedback_context[chat_id]['response_message_id']
            
            # Clear context
            del self.feedback_context[chat_id]
            
            # Update feedback with comment
            self.feedback_manager.save_feedback(
                user_id=chat_id,
                message_id=response_msg_id,
                rating=rating,
                comment=message_text
            )
            
            return "Спасибо за подробный отзыв! Мы обязательно учтём его для улучшения."

        return ""
    
    def _parse_rating(self, text: str) -> Optional[int]:
        """
        Parse rating from text (1-5)
        """
        text = text.strip().lower()
        
        # Extract number
        for word in text.split():
            if word.isdigit():
                num = int(word)
                if 1 <= num <= 5:
                    return num
        
        # Check for star emojis
        star_count = text.count('⭐') + text.count('★')
        if 1 <= star_count <= 5:
            return star_count
            
        return None
    
    def _now_iso(self) -> str:
        """
        Get current time in ISO format
        """
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()