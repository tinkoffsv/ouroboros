from .knowledge_integrator import integrate_knowledge
from .inventory_query import query_inventory
from .response_formatter import format_response

def process_meta_query(query: str) -> str:
    """
    Process a user query about META architecture.
    
    Args:
        query: User question in natural language
    
    Returns:
        Formatted response with answer and sources
    """
    # Integrate organizational knowledge
    knowledge_context = integrate_knowledge(query)
    
    # Check if database query is needed
    if "систем" in query.lower() or "владелец" in query.lower() or "criticality" in query.lower():
        inventory_data = query_inventory(query)
        knowledge_context += f"\nInventory data: {inventory_data}"
    
    # Format final response
    return format_response(query, knowledge_context)