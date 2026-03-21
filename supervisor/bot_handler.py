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
    
    def should_request_feedback(self, chat_id: int) -> bool:
        """
        Check if feedback should be requested for this chat
        """
        if chat_id == self.owner_id:
            return False  # No feedback for owner
        return True
    
    def handle_feedback_request(self, chat_id: int, response_message_id: int) -> str:
        """
        Send feedback request after a support response
        """
        if not self.should_request_feedback(chat_id):
            return ""

        # Store context to expect rating
        self.feedback_context[chat_id] = {
            'expecting_rating': True,
            'response_message_id': response_message_id,
            'timestamp': self._now_iso()
        }
        
        return "Пожалуйста, оцените это сообщение: 1-5 ★ (5 — отлично, 1 — бесполезно). Если поставите 3 или ниже — напишите, пожалуйста, почему."
    
    def handle_feedback_submission(self, chat_id: int, message_text: str) -> str:
        """
        Handle user's feedback submission (rating or comment)
        """
        if chat_id not in self.feedback_context:
            return ""

        context = self.feedback_context[chat_id]
        
        if context.get('expecting_rating'):
            # Try to parse rating
            rating = self._parse_rating(message_text)
            if rating is not None:
                # Save rating only for now
                self.feedback_manager.save_feedback(
                    user_id=chat_id,
                    message_id=context['response_message_id'],
                    rating=rating
                )
                
                if rating <= 3:
                    # Ask for comment
                    context['expecting_rating'] = False
                    context['expecting_comment'] = True
                    context['rating'] = rating
                    return "Спасибо за оценку. Пожалуйста, укажите, что именно было не так — это поможет мне улучшиться."
                else:
                    # High rating - just thank
                    del self.feedback_context[chat_id]
                    return "Спасибо за высокую оценку! 😊"
        
        elif context.get('expecting_comment'):
            # Save comment with rating
            self.feedback_manager.save_feedback(
                user_id=chat_id,
                message_id=context['response_message_id'],
                rating=context['rating'],
                comment=message_text
            )
            del self.feedback_context[chat_id]
            return "Спасибо за обратную связь — я учусь на этом."
            
        return ""

    def _parse_rating(self, text: str) -> Optional[int]:
        """
        Parse rating from text (1-5)
        """
        text = text.strip()
        
        # Try direct number
        if text.isdigit():
            rating = int(text)
            if 1 <= rating <= 5:
                return rating

        # Try with ★
        if '★' in text:
            clean = ''.join(filter(str.isdigit, text))
            if clean and clean.isdigit():
                rating = int(clean)
                if 1 <= rating <= 5:
                    return rating

        return None
    
    def _now_iso(self) -> str:
        """
        Get current time in ISO format
        """
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()