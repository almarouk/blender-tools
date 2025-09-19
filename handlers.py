"""
Handler system for Blender Node monitoring.

Provides a base handler interface and dispatcher for processing node tree changes.
"""

import bpy
from bpy.app.handlers import persistent
from abc import ABC, abstractmethod
from typing import Set, List
from functools import partial


class NodeTreeHandler(ABC):
    """Base class for node tree handlers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the handler name for identification."""
        pass

    @abstractmethod
    def should_process_tree(self, node_tree: bpy.types.NodeTree) -> bool:
        """
        Check if this handler should process the given node tree.

        Args:
            node_tree: The node tree to check

        Returns:
            True if this handler should process the tree, False otherwise
        """
        pass

    @abstractmethod
    def process_tree(self, node_tree_name: str) -> None:
        """
        Process the given node tree.

        Args:
            node_tree_name: The name of the node tree to process
        """
        pass


class HandlerRegistry:
    """Registry for managing multiple node tree handlers."""

    def __init__(self):
        self._handlers: List[NodeTreeHandler] = []
        self._registered = False

    def register_handler(self, handler: NodeTreeHandler) -> None:
        """Register a new handler."""
        if handler not in self._handlers:
            self._handlers.append(handler)
            print(f"Handler '{handler.name}' registered")

    def unregister_handler(self, handler: NodeTreeHandler) -> None:
        """Unregister a handler."""
        if handler in self._handlers:
            self._handlers.remove(handler)
            print(f"Handler '{handler.name}' unregistered")

    def get_updated_node_trees(
        self, depsgraph: bpy.types.Depsgraph
    ) -> Set[bpy.types.NodeTree]:
        """
        Get updated node trees from depsgraph.

        Args:
            depsgraph: The dependency graph

        Returns:
            Set of updated node trees
        """
        updated_node_trees: Set[bpy.types.NodeTree] = set()

        for update in depsgraph.updates[:]:
            update_id: bpy.types.ID | None = getattr(update, "id", None)
            if not update_id:
                continue

            # Check if the updated object is a node tree
            if isinstance(update_id, bpy.types.NodeTree):
                updated_node_trees.add(update_id)

        return updated_node_trees

    @persistent
    def depsgraph_handler(
        self, scene: bpy.types.Scene, depsgraph: bpy.types.Depsgraph
    ) -> None:
        """
        Main depsgraph handler that dispatches to all registered handlers.
        """
        try:
            # Get updated node trees
            updated_node_trees = self.get_updated_node_trees(depsgraph)

            # Process each updated node tree with applicable handlers
            for node_tree in updated_node_trees:
                for handler in self._handlers:
                    try:
                        if handler.should_process_tree(node_tree):
                            # Use timer for better performance
                            bpy.app.timers.register(
                                partial(handler.process_tree, node_tree.name),
                                first_interval=1,
                            )
                    except Exception as e:
                        print(f"Error in handler '{handler.name}': {e}")

        except Exception as e:
            print(f"Error in depsgraph handler: {e}")

    def register(self) -> None:
        """Register the main depsgraph handler."""
        if not self._registered:
            bpy.app.handlers.depsgraph_update_post.append(self.depsgraph_handler)
            self._registered = True
            print("Handler registry registered")

    def unregister(self) -> None:
        """Unregister the main depsgraph handler."""
        if self._registered:
            if self.depsgraph_handler in bpy.app.handlers.depsgraph_update_post:
                bpy.app.handlers.depsgraph_update_post.remove(self.depsgraph_handler)
            self._registered = False
            print("Handler registry unregistered")
