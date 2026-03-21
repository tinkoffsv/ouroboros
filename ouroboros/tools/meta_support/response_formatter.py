from typing import Dict, Any

def format_response(question_type: str, content: str, source: str = "") -> str:
    """
    Format responses in a user-friendly, consistent format.
    
    Args:
        question_type (str): Type of question (e.g., 'inventory', 'knowledge', 'mixed')
        content (str): The main content to format
        source (str): Optional source of information
    
    Returns:
        str: Formatted response ready for user
    """
    if question_type == "inventory":
        return format_inventory_response(content)
    elif question_type == "knowledge":
        return format_knowledge_response(content, source)
    elif question_type == "mixed":
        return format_mixed_response(content, source)
    else:
        return content


def format_inventory_response(content: str) -> str:
    """Format inventory query responses."""
    return f"📊 ИНВЕНТАРИЗАЦИОННЫЕ ДАННЫЕ:\n\n{content}\n\n💡 Ответ основан на актуальных данных из системы инвентаризации МЕТА."


def format_knowledge_response(content: str, source: str = "") -> str:
    """Format knowledge-based responses."""
    source_line = f" (Источник: {source})" if source else ""
    return f"📘 АРХИТЕКТУРНАЯ ИНФОРМАЦИЯ:{source_line}\n\n{content}\n\n💡 Ответ основан на внутренней документации МЕТА."


def format_mixed_response(content: str, source: str = "") -> str:
    """Format responses that combine inventory data and knowledge."""
    source_line = f" (Источник: {source})" if source else ""
    return f"🔍 КОМБИНИРОВАННЫЙ ОТВЕТ:{source_line}\n\n{content}\n\n💡 Ответ объединяет данные из инвентаризации и архитектурной документации МЕТА."


def format_error(error_msg: str) -> str:
    """Format error messages for user display."""
    return f"❌ ОШИБКА:\n\n{error_msg}\n\nПожалуйста, уточните ваш вопрос или обратитесь к документации."


def format_general_response(content: str) -> str:
    """Format general informational responses."""
    return f"ℹ️ ИНФОРМАЦИЯ:\n\n{content}"