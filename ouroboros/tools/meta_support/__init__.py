"""META support tool for answering architecture questions."""

from typing import Any, Dict, List

from ouroboros.tools.registry import ToolContext, ToolEntry
from ouroboros.tools.meta_support import handler


def _meta_support_query(ctx: ToolContext, query: str) -> str:
    """Answer questions about META architecture system."""
    return handler.handle_support_query(query)


def get_tools() -> List[ToolEntry]:
    """Export meta_support_query tool for registry auto-discovery."""
    return [
        ToolEntry(
            name="meta_support_query",
            schema={
                "name": "meta_support_query",
                "description": "Answer first-line support questions about the META architecture system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's question about META architecture, inventory, or standards."
                        }
                    },
                    "required": ["query"]
                }
            },
            handler=_meta_support_query,
            timeout_sec=30
        )
    ]
