"""
Keymap registration for the addon
"""

from __future__ import annotations

__all__ = ["register", "unregister"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bpy.types import KeyMap, KeyMapItem

import bpy
from dataclasses import dataclass
from ..operators import HideResizeNode


@dataclass
class KeyMapItemArgs:
    idname: str
    type: str
    value: str
    shift: bool = False
    ctrl: bool = False
    alt: bool = False
    repeat: bool = False
    head: bool = False


_addon_keymaps: list[tuple[KeyMap, KeyMapItem]] = []
_kmi_defs: list[KeyMapItemArgs] = [
    KeyMapItemArgs(
        idname=HideResizeNode.bl_idname,
        type="H",
        value="DOUBLE_CLICK",
    )
]


def register():
    global _addon_keymaps, _kmi_defs
    _addon_keymaps.clear()
    wm = bpy.context.window_manager
    if wm:
        kc = wm.keyconfigs.addon
        if kc:
            km = kc.keymaps.new(name="Node Editor", space_type="NODE_EDITOR")
            for kmi_def in _kmi_defs:
                kmi = km.keymap_items.new(
                    kmi_def.idname,
                    kmi_def.type,  # type: ignore
                    kmi_def.value,  # type: ignore
                    shift=kmi_def.shift,
                    ctrl=kmi_def.ctrl,
                    alt=kmi_def.alt,
                    repeat=kmi_def.repeat,
                    head=kmi_def.head,
                )
                _addon_keymaps.append((km, kmi))


def unregister():
    global _addon_keymaps
    for km, kmi in _addon_keymaps:
        km.keymap_items.remove(kmi)
    _addon_keymaps.clear()
