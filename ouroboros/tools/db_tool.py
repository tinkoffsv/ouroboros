"""Database query tool for direct SQLite access to inventory.db."""

import json
import sqlite3
from typing import Any, Dict, List, Optional

from ouroboros.tools.registry import ToolContext, ToolEntry


def _db_query(
    ctx: ToolContext,
    query: str,
    db_name: str = "inventory",
    params: Optional[List[Any]] = None
) -> str:
    """Execute SELECT query against local database and return JSON results."""
    db_map = {
        "inventory": ctx.drive_path("local_db/inventory.db"),
    }
    
    if db_name not in db_map:
        return json.dumps({"error": f"Unknown database: {db_name}. Available: {list(db_map.keys())}"})
    
    db_path = db_map[db_name]
    if not db_path.exists():
        return json.dumps({"error": f"Database not found: {db_path}"})
    
    try:
        with sqlite3.connect(str(db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, tuple(params))
            else:
                cursor.execute(query)
            
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
            
            return json.dumps(results, ensure_ascii=False, indent=2)
            
    except sqlite3.Error as e:
        return json.dumps({"error": f"SQLite error: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"Query failed: {str(e)}"})


def get_tools() -> List[ToolEntry]:
    """Export db_query tool for registry auto-discovery."""
    return [
        ToolEntry(
            name="db_query",
            schema={
                "name": "db_query",
                "description": "Execute SELECT query against local SQLite database (inventory.db). Returns JSON array of row dictionaries.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL SELECT query to execute. Use ? placeholders for parameters."
                        },
                        "db_name": {
                            "type": "string",
                            "description": "Database name (default: 'inventory'). Available: inventory",
                            "default": "inventory"
                        },
                        "params": {
                            "type": "array",
                            "description": "Optional query parameters for ? placeholders",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["query"]
                }
            },
            handler=_db_query,
            timeout_sec=30
        )
    ]