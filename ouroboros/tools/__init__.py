"""
Ouroboros — tools package.

Plugins: each module here exports get_tools() -> List[ToolEntry].
Registry auto-discovers them via pkgutil.iter_modules() at runtime.

No explicit imports needed — registry.py handles discovery.
"""

__all__ = []