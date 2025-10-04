from __future__ import annotations

from .src import (
    node_tree_handlers,
    operators,
    interface,
    properties,
)


def register():
    """Register all handlers."""
    properties.register()
    operators.register()
    interface.register()
    node_tree_handlers.register()


def unregister():
    """Unregister all handlers."""
    node_tree_handlers.unregister()
    interface.unregister()
    operators.unregister()
    properties.unregister()


if __name__ == "__main__":
    register()
