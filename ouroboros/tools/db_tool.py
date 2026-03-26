import sqlite3
import json
from typing import Any, Dict, List, Optional, Union


class DatabaseTool:
    """
    Provides direct SQLite access to Ouroboros databases, primarily inventory.db.
    Designed to replace bloated JSON state files with structured, queryable storage.
    """

    def __init__(self, db_path: str = "/home/user1/ouroboros_data/local_db/inventory.db"):
        self.db_path = db_path

    def db_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results as a list of dictionaries.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row  # This allows column access by name
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            return [{"error": f"Query failed: {str(e)}"}]

    def get_tools(self):
        return [self.db_query]