"""
Feedback module for Ouroboros Supervisor.

Manages collection and storage of user feedback (1-5★ ratings and comments).
"""

class FeedbackManager:
    """
    Collects and stores user feedback for support responses.
    """
    
    def __init__(self, storage_path: str = "memory/feedback/data"):
        self.storage_path = storage_path
        self._ensure_storage()
        
    def _ensure_storage(self):
        """
        Ensure feedback storage directory exists.
        """
        import os
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path, exist_ok=True)
            # Create .gitkeep
            keep_path = os.path.join(self.storage_path, ".gitkeep")
            if not os.path.exists(keep_path):
            with open(keep_path, 'w') as f:
                f.write("# Persistent feedback storage directory\n")
                
    def record_feedback(self, user_id: str, message_id: str, rating: int, comment: str = "") -> bool:
        """
        Record user feedback for a specific response.
        
        Args:
            user_id: Telegram user ID
            message_id: ID of the message being rated
            rating: 1-5 star rating
            comment: Optional comment (required if rating <= 3)
            
        Returns:
            bool: True if recorded successfully
        """
        import json
        import os
        from datetime import datetime
        
        # Validate rating
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
            
        # Validate comment for low ratings
        if rating <= 3 and not comment.strip():
            raise ValueError("Comment is required for ratings 1-3")
            
        # Create record
        record = {
            "user_id": user_id,
            "message_id": message_id,
            "rating": rating,
            "comment": comment.strip(),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0"
        }
        
        # Save to file
        filename = f"feedback_{user_id}_{message_id}.json"
        filepath = os.path.join(self.storage_path, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving feedback: {e}")
            return False
            
    def get_feedback_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of collected feedback.
        
        Returns:
            Dict with summary stats
        """
        import os
        import json
        
        summary = {
            "total": 0,
            "by_rating": {str(i): 0 for i in range(1, 6)},
            "with_comments": 0,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        if not os.path.exists(self.storage_path):
            return summary
            
        for filename in os.listdir(self.storage_path):
            if filename.startswith("feedback_") and filename.endswith(".json"):
                try:
                    with open(os.path.join(self.storage_path, filename), 'r') as f:
                        data = json.load(f)
                        
                    summary["total"] += 1
                    rating = str(data["rating"])
                    summary["by_rating"][rating] += 1
                    
                    if data["comment"]:
                        summary["with_comments"] += 1
                        
                except Exception as e:
                    print(f"Error reading feedback file {filename}: {e}")
                    
        return summary