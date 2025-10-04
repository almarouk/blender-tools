from __future__ import annotations

from .src import (
    handlers,
    operators,
    interface,
    properties,
    preferences,
)


def register():
    """Register all handlers."""
    properties.register()
    operators.register()
    interface.register()
    preferences.register()
    handlers.register()


def unregister():
    """Unregister all handlers."""
    interface.unregister()
    handlers.unregister()
    operators.unregister()
    properties.unregister()
    preferences.unregister()


if __name__ == "__main__":
    register()
