from __future__ import annotations

from .handlers import HandlerRegistry
from .seed_handler import SeedRandomizerHandler
from .single_socket_handler import SingleSocketHandler


def register():
    """Register all handlers."""
    # Global handler registry instance
    global handler_registry
    handler_registry = HandlerRegistry()
    handler_registry.register_handler(SeedRandomizerHandler())
    handler_registry.register_handler(SingleSocketHandler())
    handler_registry.register()


def unregister():
    """Unregister all handlers."""
    global handler_registry
    if handler_registry:
        handler_registry.unregister()
        handler_registry = None


if __name__ == "__main__":
    register()
