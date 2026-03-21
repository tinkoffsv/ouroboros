from typing import Dict, Any
from tools import knowledge_read

def integrate_knowledge(query: str) -> str:
    """
    Integrate knowledge from multiple sources to answer user questions about META.
    
    This function searches across multiple knowledge topics to provide
    comprehensive, context-aware answers to architectural questions.
    
    Args:
        query (str): User's question about META architecture
    
    Returns:
        str: Formatted response with knowledge from relevant topics
    """
    query_lower = query.lower()
    
    try:
        if "api" in query_lower and "meta" in query_lower:
            # Check for API-related questions
            knowledge = knowledge_read('meta-api-access')
            return "Based on internal documentation:\n" + knowledge
        
        elif "architecture" in query_lower or "meta model" in query_lower or "meta-model" in query_lower:
            knowledge = knowledge_read('meta-architecture')
            return "Key points about META architecture:\n" + knowledge
        
        elif "inventory" in query_lower or "system" in query_lower or "catalog" in query_lower:
            # For general system questions, check both architecture and schema
            arch_knowledge = knowledge_read('meta-architecture')
            schema_knowledge = knowledge_read('inventory-csv')
            return "Relevant information about META systems:\n" + arch_knowledge + "\n\nAdditional details:\n" + schema_knowledge
        
        elif "criticality" in query_lower or "high" in query_lower or "critical" in query_lower or "low" in query_lower:
            # For questions about system criticality, provide the policy context
            knowledge = knowledge_read('meta-architecture')
            return "Regarding system criticality in META:\n" + knowledge
        
        elif "support" in query_lower or "help" in query_lower or "question" in query_lower:
            # For support process questions
            knowledge = knowledge_read('meta-architecture')  
            return "How to get help with META:\n" + knowledge
        
        elif "governance" in query_lower or "standards" in query_lower or "rules" in query_lower:
            # For governance questions
            knowledge = knowledge_read('meta-architecture')
            return "META governance standards:\n" + knowledge
        
        else:
            # Default: use meta-architecture as primary source
            knowledge = knowledge_read('meta-architecture')
            return "I found relevant information:\n" + knowledge
            
    except Exception as e:
        return f"Error retrieving knowledge: {str(e)}"


def list_available_knowledge() -> Dict[str, str]:
    """
    List all available knowledge topics that can be queried.
    
    Returns:
        Dict mapping topic names to brief descriptions
    """
    return {
        "meta-architecture": "Core architecture of META system",
        "meta-api-access": "API access policies and procedures",
        "inventory-csv": "Schema and content of the inventory database"
    }
