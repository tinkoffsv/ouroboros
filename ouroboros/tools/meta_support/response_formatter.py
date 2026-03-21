def format_response(query: str, context: str) -> str:
    """
    Format a structured response to a META architecture query.
    
    Args:
        query: Original user question
        context: Combined knowledge and data context
    
    Returns:
        Formatted response
    """
    return f"Ответ на ваш вопрос: '{query}'\n\n{context}\n\nОтвет сформирован на основе актуальной информации из системы МЕТА."
