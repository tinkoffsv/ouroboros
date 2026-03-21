from supervisor.local_db_manager import DatabaseManager

def query_inventory(sql_query: str) -> str:
    """
    Execute a read-only SQL query against the inventory database.
    Returns results as a formatted string.
    """
    try:
        db = DatabaseManager()
        results = db.execute_query(sql_query)
        db.close()
        
        if not results:
            return "Запрос выполнен, но данные не найдены."
            
        # Format results
        output = []
        for row in results:
            output.append(" | ".join(str(v) for v in row))
        
        return "\n".join(output)
    
    except Exception as e:
        return f"Ошибка выполнения запроса: {str(e)}"
