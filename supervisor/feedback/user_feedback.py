from __future__ import annotations

import datetime
import json
import logging
import pathlib
from typing import Dict, Any, Optional

class UserFeedbackManager:
    """
    Manages user feedback collection and storage.
    """

    def __init__(self, drive_root: pathlib.Path):
        self.drive_root = drive_root
        self.feedback_dir = drive_root / "memory" / "feedback"
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        self.log = logging.getLogger(__name__)

    def store_feedback(self, user_id: str, task_id: str, rating: int, comment: Optional[str] = None) -> None:
        """
        Store user feedback for a specific task.
        """
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
            
        feedback = {
            "user_id": user_id,
            "task_id": task_id,
            "rating": rating,
            "comment": comment,
            "timestamp": json.dumps(datetime.datetime.now(datetime.timezone.utc), default=str)
        }
        
        file_path = self.feedback_dir / f"{user_id}_{task_id}.json"
        try:
            file_path.write_text(json.dumps(feedback, ensure_ascii=False, indent=2), encoding="utf-8")
            self.log.info(f"Stored feedback for user {user_id}, task {task_id}")
        except Exception as e:
            self.log.error(f"Failed to store feedback: {e}")
            
    def get_feedback_stats(self) -> Dict[str, Any]:
        """
        Return statistics about collected feedback.
        """
        stats = {
            "total_feedback": 0,
            "average_rating": 0.0,
            "ratings": {i: 0 for i in range(1, 6)}
        }
        
        if not self.feedback_dir.exists():
            return stats
            
        feedback_files = list(self.feedback_dir.glob("*.json"))
        stats["total_feedback"] = len(feedback_files)
        
        total_score = 0
        for file_path in feedback_files:
            try:
                data = json.loads(file_path.read_text(encoding="utf-8"))
                rating = data.get("rating", 0)
                if 1 <= rating <= 5:
                    stats["ratings"][rating] += 1
                    total_score += rating
            except Exception as e:
                self.log.error(f"Failed to read feedback file {file_path}: {e}")

        if stats["total_feedback"] > 0:
            stats["average_rating"] = total_score / stats["total_feedback"]
            
        return stats