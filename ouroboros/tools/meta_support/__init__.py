"""
Meta Support Agent — A specialized first-line support tool for META architecture inquiries.
"""

def get_tools():
    """Return list of available tools."""
    from .handler import process_meta_query
    return [
        {"name": "process_meta_query", "function": process_meta_query}
    ]