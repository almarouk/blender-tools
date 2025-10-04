"""
Interface elements such as panels and menus.
"""

from __future__ import annotations

__all__ = ["register", "unregister"]

from . import menus, keymaps


def register():
    menus.register()
    keymaps.register()


def unregister():
    keymaps.unregister()
    menus.unregister()
