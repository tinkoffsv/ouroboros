from typing import Dict, Any
import logging

class UserFeedbackManager:
    """
    Manages feedback collection from support users.
    Implements 1-5 star rating with optional comments for ratings 3 and below.
    """
    
    def __init__(self, storage_path: str = "memory/feedback"):
        self.storage_path = storage_path
        self.log = logging.getLogger(__name__)
        self._ensure_storage_dir()
    
    def _ensure_storage_dir(self):
        """Ensure feedback storage directory exists"""
        import os
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path, exist_ok=True)
    
    def request_feedback(self, user_id: int, message_id: int, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request feedback from user after a support response.
        
        Returns structured feedback request.
        """
        return {
            "user_id": user_id,
            "message_id": message_id,
            "request_id": f"fb_{user_id}_{message_id}",
            "context": context,
            "prompt": "Оцените, насколько ответ был полезен: 1-5 ★",
            "options": ["1 ★", "2 ★", "3 ★", "4 ★", "5 ★"],
            "request_type": "rating"
        }
    
    def process_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process received feedback.
        If rating <= 3, ask for comment.
        """
        rating = feedback_data.get("rating")
        user_id = feedback_data.get("user_id")
        message_id = feedback_data.get("message_id")
        
        if rating is None:
            self.log.warning(f"Missing rating in feedback data: {feedback_data}")
            return {"status": "error", "message": "Rating is required"}
        
        # Save feedback
        self._save_feedback(feedback_data)
        
        # If low rating, request comment
        if rating <= 3:
            return {
                "follow_up": True,
                "request_id": f"comment_{user_id}_{message_id}",
                "prompt": "Пожалуйста, уточните, что было не так или что можно улучшить:" 
            }
        
        return {
            "follow_up": False,
            "message": "Спасибо за высокую оценку!"
        }
    
    def _save_feedback(self, feedback_data: Dict[str, Any]):
        """Save feedback to storage"""
        import json
        import os
        from datetime import datetime
        
        filename = f"{self.storage_path}/{feedback_data['user_id']}_{feedback_data['message_id']}.json"
        
        data = {
            "timestamp": datetime.utcnow().isoformat(),
            "saved_at": datetime.now().isoformat(),
            **feedback_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.log.info(f"Feedback saved: {filename}")
    
    def get_feedback_stats(self) -> Dict[str, Any]:
        """Get feedback statistics"""
        import os
        import json
        
        stats = {
            "total": 0,
            "by_rating": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            "average_rating": 0.0
        }
        
        if not os.path.exists(self.storage_path):
            return stats
            
        files = [f for f in os.listdir(self.storage_path) if f.endswith('.json')]
        
        for file in files:
            try:
                with open(f"{self.storage_path}/{file}", 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    rating = data.get('rating')
                    if rating:
                        stats["total"] += 1
                        stats["by_rating"][rating] += 1
            except Exception as e:
                self.log.error(f"Error reading feedback file {file}: {e}")
        
        if stats["total"] > 0:
            total_rating = sum(r * c for r, c in stats["by_rating"].items())
            stats["average_rating"] = round(total_rating / stats["total"], 2)
            
        return stats