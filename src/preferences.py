from __future__ import annotations

__all__ = ["register", "unregister", "get_preferences", "draw_preferences"]

from typing import TYPE_CHECKING, cast, Iterable
import bpy
from bpy.props import BoolProperty, CollectionProperty, StringProperty  # type: ignore
from bpy.types import AddonPreferences, PropertyGroup, UIList
from bpy.utils import register_class, unregister_class
from .. import __package__ as pkg

ADDON_ID = cast(str, pkg)

if TYPE_CHECKING:
    from bpy.types import Context, bpy_prop_collection_idprop, UILayout
    from .utils.handlers import BaseNodeTreeHandler


def get_preferences(context: Context | None = None) -> Preferences:
    if context is None:
        context = bpy.context
    if context.preferences is None:
        raise RuntimeError("Blender preferences not found")
    addon = context.preferences.addons.get(ADDON_ID)
    if addon is None:
        raise RuntimeError("Addon preferences not found")
    prefs = cast("Preferences", addon.preferences)
    return prefs


def draw_preferences(
    layout: UILayout, prefs: Preferences | None = None, compact: bool = True
) -> None:
    if prefs is None:
        prefs = get_preferences()
    nb_col = 1 if compact else 2
    grid = layout.grid_flow(row_major=True, columns=nb_col)

    row = grid.row(align=True)
    if compact:
        row = row.column(align=True)
    row.label(text="Node Tree Handlers:")
    if not prefs.handler_settings:
        row.label(text="No handlers available", icon="INFO")
    else:
        row.template_list(
            "NODETREE_UL_handler_preferences",
            "",
            prefs,
            "handler_settings",
            prefs,
            "active_handler_index",
        )


class NodeTreeHandlerPreference(PropertyGroup):
    idname: StringProperty(  # type: ignore
        name="ID Name",
        description="Identifier of the node tree handler",
        options={"HIDDEN"},
    )
    label: StringProperty(  # type: ignore
        name="Label",
        description="Display name of the handler",
        default="",
        options={"HIDDEN"},
    )
    enabled: BoolProperty(  # type: ignore
        name="Enabled",
        description="Enable this handler when node trees are updated",
        default=True,
    )

    if TYPE_CHECKING:
        idname: str
        label: str
        enabled: bool


class NodeTreeHandlerPreferences(UIList):
    """UIList to display node tree handler preferences"""

    bl_idname = "NODETREE_UL_handler_preferences"

    def draw_item(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        context: Context,
        layout: UILayout,
        data: Preferences,
        item: NodeTreeHandlerPreference,
        icon: int,
        active_data: Preferences,
        active_property: str,
        index: int,
        flt_flag: int,
    ) -> None:
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            layout.prop(item, "enabled", text="")
            layout.label(text=item.label)
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="")


class Preferences(AddonPreferences):
    bl_idname = ADDON_ID

    handler_settings: CollectionProperty(  # type: ignore
        name="Node Tree Handlers",
        description="Preferences for automated node tree handlers",
        type=NodeTreeHandlerPreference,
    )
    active_handler_index: bpy.props.IntProperty(  # type: ignore
        name="Active Handler Index",
        description="Index of the active node tree handler",
        default=0,
        options={"HIDDEN", "SKIP_SAVE", "SKIP_PRESET"},
    )

    if TYPE_CHECKING:
        handler_settings: bpy_prop_collection_idprop[NodeTreeHandlerPreference]
        # handler_settings: list[NodeTreeHandlerPreference]
        active_handler_index: int

    def register_handlers(self, classes: Iterable[type[BaseNodeTreeHandler]]) -> None:
        existing_ids = {h.idname for h in self.handler_settings}
        for cls in classes:
            if cls.bl_idname not in existing_ids:
                item = self.handler_settings.add()
                item.idname = cls.bl_idname
                item.label = cls.bl_label
                item.enabled = True
                existing_ids.add(cls.bl_idname)

    def get_active_handlers(self) -> list[str]:
        return [h.idname for h in self.handler_settings if h.enabled]

    def draw(self, context: Context) -> None:
        layout = self.layout
        draw_preferences(layout, self, compact=False)


classes = (
    NodeTreeHandlerPreference,
    NodeTreeHandlerPreferences,
    Preferences,
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
