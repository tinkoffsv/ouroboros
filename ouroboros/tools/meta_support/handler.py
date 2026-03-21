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
    knowledge_fragments = integrate_knowledge(query)
    
    # Check if database query is needed and synthesize SQL
    inventory_data = ""
    if any(term in query.lower() for term in ["систем", "владелец", "criticality", "тех лид", "lifecycle"]):
        # Extract system name if mentioned
        system_name = None
        if "hr portal" in query.lower():
            system_name = "HR Portal"
        # Add other system name mappings here as needed
        
        if system_name:
            sql = f"SELECT * FROM inventory WHERE system_name = '{system_name}'"
        else:
            sql = "SELECT COUNT(*) FROM inventory"
            
        inventory_data = query_inventory(sql)
    
    # Format final response
    answer = f"Найдено в базе знаний:\n{knowledge_fragments}"
    if inventory_data:
        answer += f"\n\nДанные из инвентаризации:\n{inventory_data}"
        
    return format_response(answer, "META Support Agent")
