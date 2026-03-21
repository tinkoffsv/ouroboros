import json
import datetime
import os
from typing import Dict, Any

class UserFeedbackManager:
    """
    Manages user feedback for support interactions.
    Stores ratings (1-5 stars) and optional comments.
    """

    def __init__(self, data_dir: str = "memory/feedback/data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def save_feedback(self, user_id: int, message_id: int, rating: int, comment: str = ""):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        feedback = {
            "user_id": user_id,
            "message_id": message_id,
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        
        file_path = os.path.join(self.data_dir, f"feedback_{user_id}_{message_id}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(feedback, f, ensure_ascii=False, indent=2)
            
        return file_path

    def get_feedback(self, feedback_id: str) -> Dict[str, Any]:
        """
        Retrieve saved feedback by ID
        """
        file_path = os.path.join(self.data_dir, f"{feedback_id}.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Feedback {feedback_id} not found")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_feedback(self) -> list:
        """
        List all available feedback files
        """
        if not os.path.exists(self.data_dir):
            return []
            
        files = []
        for filename in os.listdir(self.data_dir):
            if filename.startswith("feedback_") and filename.endswith(".json"):
                files.append(filename)
                
        return files