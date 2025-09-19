import bpy
from .handlers import NodeTreeHandler


class SingleSocketHandler(NodeTreeHandler):
    """Hides group input/output nodes with only one visible socket and sets their label to the socket name."""

    @property
    def name(self) -> str:
        """Returns the handler's display name."""
        return "Single Socket Handler"

    def should_process_tree(self, node_tree: bpy.types.NodeTree) -> bool:
        """Returns True for all node trees."""
        return True

    def process_tree(self, node_tree_name: str) -> None:
        """Hides group input/output nodes with exactly one visible socket and sets their label."""
        try:
            node_tree: bpy.types.NodeTree | None = bpy.data.node_groups.get(
                node_tree_name
            )
            if node_tree is None:
                print(f"Node tree '{node_tree_name}' not found")
                return

            for node in node_tree.nodes[:]:
                try:
                    sockets: list[bpy.types.NodeSocket]
                    if isinstance(node, bpy.types.NodeGroupInput):
                        sockets = node.outputs[:]
                    elif isinstance(node, bpy.types.NodeGroupOutput):
                        sockets = node.inputs[:]
                    else:
                        continue

                    visible_sockets = [socket for socket in sockets if not socket.hide]
                    if len(visible_sockets) != 1:
                        continue
                    socket = visible_sockets[0]
                    if node.label != socket.name or not node.hide:
                        node.label = socket.name
                        node.hide = True
                except Exception as e:
                    print(f"Error processing node '{node.name}': {e}")
                    continue
        except Exception as e:
            print(f"Error processing node tree '{node_tree_name}': {e}")
