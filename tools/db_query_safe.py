import json
import sqlite3
import os
from typing import Any, Dict, List

from ouroboros.tools import ToolRegistry


def db_query_safe(sql_query: str, db_path: str = None) -> str:
    """
    Execute a SQL SELECT query on the local SQLite database with strict security controls.
    
    Args:
        sql_query: The SQL SELECT query string.
        db_path: Optional path to the SQLite database. If not provided, uses inventory.db location.
    
    Returns:
        JSON string containing query results as list of dicts or error object.
    """
    if not isinstance(sql_query, str):
        return json.dumps({"error": "SQL query must be a string."})
        
    # Ensure query starts with SELECT (case-insensitive)
    if not sql_query.strip().upper().startswith('SELECT'):
        return json.dumps({"error": "Only SELECT queries are allowed."})

    # Use provided db_path or default to inventory.db
    if db_path is None:
        db_path = os.path.join(ToolRegistry._ctx.repo_dir, '..', 'ouroboros_data', 'local_db', 'inventory.db')
    
    try:
        with sqlite3.connect(db_path, timeout=10) as conn:
            # Set row factory for better dictionary conversion
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Add query timeout
            cursor.execute("PRAGMA query_timeout = 5000")
            
            # Execute query
            cursor.execute(sql_query)
            
            # Limit result size
            results = cursor.fetchmany(1000)  
            
            return json.dumps([dict(row) for row in results])
            
    except sqlite3.Error as e:
        return json.dumps({"error": f"Database error: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"})


def get_tools() -> Dict[str, Any]:
    return {
        "db_query_safe": db_query_safe
    }