from __future__ import annotations

from .src import node_tree_handlers, operators


def register():
    """Register all handlers."""
    node_tree_handlers.register()
    operators.register()


def unregister():
    """Unregister all handlers."""
    node_tree_handlers.unregister()
    operators.unregister()


if __name__ == "__main__":
    register()
