def format_response(answer: str, source: str = "") -> str:
    """
    Format the final response for user delivery.
    """
    if source:
        return f"{answer}\n\nИсточник: {source}"
    return answer
        
def format_error(error: str) -> str:
    """
    Format error messages for user delivery.
    """
    return f"⚠️ {error}"
