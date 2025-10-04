from __future__ import annotations

__all__ = ["HideResizeNode"]

from typing import TYPE_CHECKING
from .. import utils

if TYPE_CHECKING:
    from bpy.types import Context


class HideResizeNode(utils.operators.BaseOperator):
    """Hide nodes, their unused sockets, and resize to minimum width"""

    bl_idname = "node.hide_socket_resize_toggle"
    bl_label = "Hide and Resize Nodes"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def _poll(cls, context: Context):
        nodes = utils.nodes.get_selected_nodes(context)
        if isinstance(nodes, str):
            return nodes

    def _execute(self, context: Context):
        # bpy.ops.node.hide_socket_toggle()
        # bpy.ops.node.hide_toggle()

        # Resize selected nodes to minimum width if hidden, else reset to default width
        for node in context.selected_nodes:
            if node.hide:
                node.width = node.bl_width_min
            else:
                node.width = node.bl_width_default
