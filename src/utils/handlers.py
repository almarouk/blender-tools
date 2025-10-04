from __future__ import annotations

__all__ = ["BaseNodeTreeHandler"]

from typing import TYPE_CHECKING
from abc import abstractmethod
import bpy
from .nodes import get_node_tree
from .operators import BaseOperator
from bpy.props import StringProperty  # type: ignore

if TYPE_CHECKING:
    from bpy.types import Context, NodeTree


class BaseNodeTreeHandler(BaseOperator):
    node_tree_name: StringProperty(  # type: ignore
        name="Node Tree Name",
        description="Name of the node tree to operate on (overrides context)",
        default="",
        options={"SKIP_SAVE", "HIDDEN"},
    )
    if TYPE_CHECKING:
        node_tree_name: str = ""

    @abstractmethod
    def _execute_node_tree(
        self, node_tree: NodeTree
    ) -> tuple[set[str], str] | set[str] | str | None: ...

    @classmethod
    @abstractmethod
    def _poll_node_tree(cls, node_tree: NodeTree) -> str | None: ...

    @classmethod
    def poll_node_tree(cls, node_tree_name: str) -> bool:
        node_tree = bpy.data.node_groups.get(
            node_tree_name, f"Node tree '{node_tree_name}' not found."
        )
        if isinstance(node_tree, str):
            msg = node_tree
        else:
            msg = cls._poll_node_tree(node_tree)
        if isinstance(msg, str):
            cls.poll_message_set(msg)
            return False
        return True

    @classmethod
    def _poll(cls, context: Context):
        pass
        # node_tree = get_node_tree(context)
        # if isinstance(node_tree, str):
        #     return node_tree
        # msg = cls._poll_node_tree(node_tree)
        # if isinstance(msg, str):
        #     return msg

    def _execute(self, context: Context):
        if self.node_tree_name:
            node_tree = bpy.data.node_groups.get(
                self.node_tree_name, f"Node tree '{self.node_tree_name}' not found."
            )
        else:
            node_tree = get_node_tree(context)
        if isinstance(node_tree, str):
            msg = node_tree
        else:
            msg = self._poll_node_tree(node_tree)
        if isinstance(msg, str):
            self.poll_message_set(msg)
            return msg

        return self._execute_node_tree(node_tree)
