from .knowledge_integrator import integrate_knowledge
from .inventory_query import query_inventory
from .response_formatter import format_response, format_error, format_general_response
from typing import Dict, Any

def handle_support_query(query: str) -> str:
    """
    Handle a user query for the META first-line support agent.
    
    This is the main orchestrator that routes queries to the appropriate
    data sources and formats the response.
    
    Args:
        query (str): User's natural language question
    
    Returns:
        str: Formatted response for the user
    """
    query_lower = query.lower().strip()
    
    # Handle simple greeting/start commands
    if query_lower in ['/start', '/hello', 'start', 'привет', 'здравствуйте', 'hi', 'hello', 'good morning', 'доброе утро']:
        return "Hi, it is META support. What do you want?"
    
    # Handle other basic greeting variations
    if query_lower in ['hello', 'hi there', 'hey', 'приветик', 'здарова']:
        return "Hi, it is META support. What do you want?"
    
    try:
        # Determine query type based on keywords
        needs_inventory = any(kw in query_lower for kw in ['criticality', 'high', 'critical', 'medium', 'low', 'system', 'backend', 'node.js', 'list all'])
        needs_knowledge = any(kw in query_lower for kw in ['api', 'architecture', 'model', 'standards', 'governance', 'support', 'help', 'process'])
        
        if needs_inventory and needs_knowledge:
            # Mixed query - get both data and knowledge
            inventory_result = query_inventory(query)
            knowledge_result = integrate_knowledge(query)
            combined = f"{inventory_result}\n\nДополнительный контекст:\n{knowledge_result}"
            return format_response('mixed', combined, 'meta-architecture')
            
        elif needs_inventory:
            # Pure inventory query
            result = query_inventory(query)
            return format_response('inventory', result)
            
        elif needs_knowledge:
            # Pure knowledge query
            result = integrate_knowledge(query)
            return format_response('knowledge', result, 'meta-architecture')
            
        else:
            # Default response for unrecognized queries
            general_info = "Я — агент поддержки МЕТА. Готов помочь с вопросами по архитектуре, инвентаризации и стандартам.\n\nПримеры вопросов:\n- «Сколько систем с критичностью High?»\n- «Как узнать владельца CRM Core?»\n- «Есть ли у МЕТА API?»\n- «Как сообщить о проблеме в МЕТА?»"
            return format_general_response(general_info)
            
    except Exception as e:
        error_msg = f"Произошла ошибка при обработке запроса: {str(e)}"
        return format_error(error_msg)


def get_agent_status() -> Dict[str, Any]:
    """
    Get status information about the support agent.
    
    Returns:
        Dict with agent status and capabilities
    """
    return {
        "status": "active",
        "capabilities": [
            "Answer questions about system criticality",
            "Provide knowledge about META architecture",
            "List systems by technology stack",
            "Explain API access policies"
        ],
        "knowledge_sources": [
            "meta-architecture",
            "meta-api-access",
            "inventory-csv"
        ]
    }