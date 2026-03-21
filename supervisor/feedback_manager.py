class UserFeedbackManager:
    """
    Manages user feedback for support interactions.
    Stores ratings (1-5 stars) and optional comments.
    """

    def __init__(self, data_dir: str):
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