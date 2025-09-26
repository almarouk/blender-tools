"""
Node tree handlers package for Blender.

Provides handlers for monitoring and processing node tree changes.
"""

__all__ = [
    "NodeTreeHandler",  # Base class for creating custom handlers
    "register",  # Main registration function
    "unregister",  # Main unregistration function
]

from .handlers import HandlerRegistry, NodeTreeHandler
from .seed_handler import SeedRandomizerHandler
from .single_socket_handler import SingleSocketHandler


# Global handler registry instance
_handler_registry = None


def register():
    """Register all node tree handlers."""
    global _handler_registry
    _handler_registry = HandlerRegistry()
    _handler_registry.register_handler(SeedRandomizerHandler())
    _handler_registry.register_handler(SingleSocketHandler())
    _handler_registry.register()


def unregister():
    """Unregister all node tree handlers."""
    global _handler_registry
    if _handler_registry:
        _handler_registry.unregister()
        _handler_registry = None
