from typing import Dict, Any
from supervisor.local_db_manager import query_systems_by_criticality, get_all_systems, get_db_connection

def query_inventory(query: str) -> str:
    """
    Process a user query about META inventory data.
    
    This function understands queries about:
    - Systems with specific criticality (High, Critical, etc.)
    - All systems information
    - Specific system attributes
    
    For security, all database queries use parameterized statements through 
    the local_db_manager.py interface, which prevents SQL injection.
    
    Args:
        query (str): User's natural language question about inventory
    
    Returns:
        str: Formatted response with inventory information or error message
    """
    query_lower = query.lower()
    
    try:
        if "criticality" in query_lower or "high" in query_lower or "critical" in query_lower or "medium" in query_lower or "low" in query_lower:
            # Extract criticality level from query
            criticality = None
            if "high" in query_lower:
                criticality = "High"
            elif "critical" in query_lower:
                criticality = "Critical"
            elif "medium" in query_lower:
                criticality = "Medium"
            elif "low" in query_lower:
                criticality = "Low"
            
            if criticality:
                systems = query_systems_by_criticality(criticality)
                if systems:
                    result = f"There are {len(systems)} systems with criticality '{criticality}':\n\n"
                    for system in systems:
                        result += f"- {system['system_id']}: {system['system_name']} (Owner: {system['owner']}, Domain: {system['domain']})\n"
                    return result
                else:
                    return f"No systems found with criticality '{criticality}'."
            
        elif "all systems" in query_lower or "all the systems" in query_lower or "list all" in query_lower:
            systems = get_all_systems()
            if systems:
                result = f"Total {len(systems)} systems in inventory:\n\n"
                for system in systems:
                    result += f"- {system['system_id']}: {system['system_name']} (Criticality: {system['criticality']}, Owner: {system['owner']})\n"
                return result
            else:
                return "No systems found in inventory."
        
        elif "backend" in query_lower and "node.js" in query_lower:
            # Query for backend containing Node.js (case-insensitive)
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT system_id, system_name, owner, criticality FROM inventory WHERE LOWER(backend) LIKE '%node.js%'",
                ()
            )
            rows = cursor.fetchall()
            conn.close()
            
            if rows:
                systems = [dict(row) for row in rows]
                result = f"There are {len(systems)} systems with backend Node.js:\n\n"
                for system in systems:
                    result += f"- {system['system_id']}: {system['system_name']} (Owner: {system['owner']}, Criticality: {system['criticality']})\n"
                return result
            else:
                return "No systems found with backend Node.js."
        
        else:
            return "I cannot answer that specific inventory question. I can help with:\n- Systems by criticality (High, Critical, etc.)\n- All systems in inventory\n- Systems with specific backend technologies"
            
    except Exception as e:
        return f"Error processing inventory query: {str(e)}"


def get_database_info() -> Dict[str, Any]:
    """
    Get metadata about the inventory database.
    
    Returns:
        Dict with database path and status
    """
    return {
        "database_path": '/home/admin/ouroboros_data/local_db/inventory.db',
        "status": "connected" if get_db_connection() else "disconnected"
    }
