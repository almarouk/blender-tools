from __future__ import annotations

__all__ = ["register", "unregister"]

from typing import TYPE_CHECKING
from bpy.types import Panel
from bpy.utils import register_class, unregister_class
from ..utils.preferences import get_preferences, draw_preferences
from ..utils.nodes import get_node_tree

if TYPE_CHECKING:
    from bpy.types import Context


class PanelBase(Panel):
    @classmethod
    def poll(cls, context: Context) -> bool:
        node_tree = get_node_tree(context)
        return not isinstance(node_tree, str)


class PreferencesPanel(PanelBase):
    bl_space_type = "NODE_EDITOR"
    bl_label = "Preferences"
    bl_region_type = "UI"
    bl_category = "Tools"

    def draw(self, context: Context) -> None:
        layout = self.layout
        if not layout:
            return
        draw_preferences(layout, get_preferences(context), compact=True)


def register():
    register_class(PreferencesPanel)


def unregister():
    unregister_class(PreferencesPanel)
