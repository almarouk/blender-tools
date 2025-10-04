"""
Interface elements such as panels and menus.
"""

from __future__ import annotations

__all__ = ["register", "unregister"]

from . import menus, keymaps, panels


def register():
    menus.register()
    keymaps.register()
    panels.register()


def unregister():
    panels.unregister()
    keymaps.unregister()
    menus.unregister()
