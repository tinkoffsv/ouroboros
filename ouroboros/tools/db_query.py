import json
import sqlite3
import os
from typing import Any, Dict, List

from ouroboros.tools import ToolRegistry

def db_query(sql_query: str, db_path: str = None) -> str:
    """
    Execute a SQL SELECT query on the local SQLite database.
    
    Args:
        sql_query: The SQL SELECT query string.
        db_path: Optional path to the SQLite database. If not provided, uses inventory.db location.
    
    Returns:
        JSON string containing query results as list of dicts or error object.
    """
    if not isinstance(sql_query, str):
        return json.dumps({"error": "SQL query must be a string."})

    # Use provided db_path or default to inventory.db
    if db_path is None:
        db_path = os.path.join(ToolRegistry._ctx.repo_dir, '..', 'ouroboros_data', 'local_db', 'inventory.db')
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            result_dicts = [dict(zip(columns, row)) for row in results]
            
            return json.dumps(result_dicts)
    except sqlite3.Error as e:
        return json.dumps({"error": f"Database error: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"})

def get_tools() -> Dict[str, Any]:
    return {
        "db_query": db_query
    }