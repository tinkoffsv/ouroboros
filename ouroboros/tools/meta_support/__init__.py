"""
Registers the meta_support tool for use by Ouroboros.
"""

from . import handler

TOOLS = [
    {
        "type": "function",
        "function": {
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
        }
    }
]

def call_tool(tool_name: str, args: Dict[str, Any]) -> str:
    """
    Call a specific tool from this module.
    
    Args:
        tool_name (str): Name of the tool to call
        args (Dict): Arguments for the tool
    
    Returns:
        str: Result of the tool execution
    """
    if tool_name == "meta_support_query":
        return handler.handle_support_query(args["query"])
    else:
        return f"Unknown tool: {tool_name}"
