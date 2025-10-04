"""
Menu definitions for the node editor.
"""

from __future__ import annotations

__all__ = ["register", "unregister"]

from typing import TYPE_CHECKING
from bpy.types import Menu, NODE_MT_context_menu
from bpy.utils import register_class, unregister_class
from ..operators import SplitMergeGroupInput

if TYPE_CHECKING:
    from bpy.types import Context


class SplitMergeGroupInputMenu(Menu):
    bl_idname = "NODE_MT_split_merge_group_input_menu"
    bl_label = "Split/Merge"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return SplitMergeGroupInput._poll(context) is None

    def draw(self, context: Context) -> None:
        layout = self.layout
        if not layout:
            return
        layout.operator_context = "INVOKE_DEFAULT"

        _ = layout.operator(SplitMergeGroupInput.bl_idname, text="Split/Merge")
        # layout.operator(
        #     SplitGroupInput.bl_idname, text="Split Grouped"
        # ).grouped_by_dest_node = True

        # layout.separator()
        # layout.operator(
        #     MergeGroupInput.bl_idname, text="Merge all"
        # ).grouped_by_dest_node = False
        # layout.operator(
        #     MergeGroupInput.bl_idname, text="Merge Grouped"
        # ).grouped_by_dest_node = True


_classes: tuple[type[Menu], ...] = (SplitMergeGroupInputMenu,)


def _draw_node_context_menu(self: Menu, context: Context) -> None:
    if not self.layout:
        return
    col = self.layout.column(align=True)
    col.operator_context = "INVOKE_DEFAULT"
    if SplitMergeGroupInput._poll(context) is None:
        _ = col.operator(SplitMergeGroupInput.bl_idname, text="Split/Merge")
    # col.menu(SplitMergeGroupInputMenu.bl_idname)
    col.separator()


def register():
    for cls in _classes:
        register_class(cls)
    NODE_MT_context_menu.prepend(_draw_node_context_menu)  # pyright: ignore[reportUnknownMemberType]


def unregister():
    NODE_MT_context_menu.remove(_draw_node_context_menu)  # pyright: ignore[reportUnknownMemberType]
    for cls in reversed(_classes):
        unregister_class(cls)
