"""
Ouroboros — tools package.

Plugins: each module here exports get_tools() -> List[ToolEntry].
Registry auto-discovers them by importlib + pkgutil.
"""

class _ToolModulePlaceholder:
    # For tests/IDE only. Not used at runtime.
    def get_tools(self):
        from ouroboros.tools.core import get_tools as core_get_tools
        return core_get_tools()

__all__ = ["_ToolModulePlaceholder"]

# Ensure db_tool is registered by importing the module
try:
    import ouroboros.tools.db_tool  # noqa: F401
except ImportError:
    pass