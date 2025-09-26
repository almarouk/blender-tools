import bpy
from bpy.types import Operator, Context, SpaceNodeEditor
from typing import cast
from dataclasses import dataclass

__all__ = ["register", "unregister"]


class HideResizeNodes(Operator):
    """Hide nodes, their unused sockets, and resize to minimum width"""

    bl_idname = "node.hide_socket_resize_toggle"
    bl_label = "Hide and Resize Nodes"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        space = context.space_data
        if space is None:
            cls.poll_message_set("No active space found.")
            return False
        if space.type != "NODE_EDITOR":
            cls.poll_message_set("Current editor is not a node editor.")
            return False
        space = cast(SpaceNodeEditor, space)
        if space.node_tree is None:
            cls.poll_message_set("No node tree was found in the current node editor.")
            return False
        if space.node_tree.library is not None:  # type: ignore
            cls.poll_message_set(
                "Current node tree is linked from another .blend file."
            )
            return False
        if not space.edit_tree or not space.edit_tree.nodes:
            cls.poll_message_set("Current node tree does not contain any nodes.")
            return False

        num_selected = len(context.selected_nodes)
        if num_selected < 1:
            cls.poll_message_set("No nodes selected.")
            return False
        return True

    def execute(self, context: Context) -> set[str]:  # type: ignore
        # bpy.ops.node.hide_socket_toggle()
        # bpy.ops.node.hide_toggle()

        # Resize selected nodes to minimum width if hidden, else reset to default width
        for node in context.selected_nodes:
            if node.hide:
                node.width = node.bl_width_min
            else:
                node.width = node.bl_width_default

        return {"FINISHED"}


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


_addon_keymaps: list[tuple[bpy.types.KeyMap, bpy.types.KeyMapItem]] = []
_kmi_defs: list[KeyMapItemArgs] = [
    KeyMapItemArgs(
        idname=HideResizeNodes.bl_idname,
        type="H",
        value="DOUBLE_CLICK",
    )
]


def register():
    global _addon_keymaps, _kmi_defs
    bpy.utils.register_class(HideResizeNodes)

    # Register keymaps
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

    # Unregister keymaps
    for km, kmi in _addon_keymaps:
        km.keymap_items.remove(kmi)
    _addon_keymaps.clear()

    bpy.utils.unregister_class(HideResizeNodes)
