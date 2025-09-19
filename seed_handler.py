"""
Node Editor Tools - Seed Randomizer Handler

Automatically inserts Random Value nodes when Seed inputs are linked in Node trees.
Monitors node updates and creates randomization nodes with unique offsets for varied outputs.
"""

import bpy
from .utils import get_node_socket_location
from .handlers import NodeTreeHandler
from typing import cast


class SeedRandomizerHandler(NodeTreeHandler):
    """Handler for automatically inserting Random Value nodes for seed inputs."""

    @property
    def name(self) -> str:
        return "Seed Randomizer"

    def process_link(
        self,
        node_tree: bpy.types.NodeTree,
        link: bpy.types.NodeLink,
        new_offset: int,
    ) -> bool:
        """
        Insert Random Value and Integer Value nodes between a seed link.

        Args:
            node_tree: node tree containing the link
            link: Node link connecting to a "Seed" input
            new_offset: Unique integer offset for the Random Value node ID

        Returns:
            True if nodes were successfully inserted, False otherwise
        """
        try:
            assert (
                link.to_socket is not None
                and link.from_socket is not None
                and link.from_socket.node is not None
                and link.to_socket.node is not None
            ), "Invalid node link"

            to_node = link.to_socket.node

            # Create Random Value node
            random_node: bpy.types.FunctionNodeRandomValue = node_tree.nodes.new(
                type="FunctionNodeRandomValue"
            )  # type: ignore
            random_node.hide = True
            random_node.select = False
            random_node.width = random_node.bl_width_min
            socket_location = get_node_socket_location(to_node, "Seed", True)
            if socket_location:
                random_node.location = (
                    socket_location[0] - random_node.width - 25,
                    socket_location[1] + 15,
                )
            else:
                random_node.location = (
                    to_node.location.x - random_node.width - 25,
                    to_node.location.y,
                )
            random_node.label = "Auto Random Seed"
            random_node.data_type = "INT"
            if to_node.parent:
                random_node.parent = to_node.parent  # type: ignore

            # Set default range for integer random values
            socket: bpy.types.NodeSocketInt = random_node.inputs["Min"]  # type: ignore
            socket.default_value = 0
            socket: bpy.types.NodeSocketInt = random_node.inputs["Max"]  # type: ignore
            socket.default_value = 1000000

            # Add an Integer Value Node
            int_value_node: bpy.types.FunctionNodeInputInt = node_tree.nodes.new(
                type="FunctionNodeInputInt"
            )  # type: ignore
            int_value_node.hide = True
            int_value_node.select = False
            int_value_node.width = int_value_node.bl_width_min
            int_value_node.location = (
                random_node.location.x - int_value_node.width - 25,
                random_node.location.y,
            )
            int_value_node.label = "Auto Random Seed Offset"
            int_value_node.integer = new_offset
            if to_node.parent:
                int_value_node.parent = to_node.parent  # type: ignore

            # Add a Group Input Node with Seed shown only
            group_input_node: bpy.types.NodeGroupInput = node_tree.nodes.new(
                type="NodeGroupInput"
            )  # type: ignore
            group_input_node.hide = True
            group_input_node.select = False
            group_input_node.width = group_input_node.bl_width_min
            group_input_node.label = "Seed"
            socket_out: bpy.types.NodeSocket
            for socket_out in group_input_node.outputs:
                if socket_out.name.strip().lower() == "seed":
                    socket_out.hide = False
                else:
                    socket_out.hide = True
            # group_input_node.location = (random_node.location.x - group_input_node.width - 25, int_value_node.location.y - int_value_node.dimensions.y - 5)
            group_input_node.location = (
                random_node.location.x - group_input_node.width - 25,
                int_value_node.location.y - int_value_node.bl_height_min - 5,
            )
            if to_node.parent:
                group_input_node.parent = to_node.parent  # type: ignore

            # Create new links through the Random Value node
            node_tree.links.new(
                group_input_node.outputs["Seed"],
                random_node.inputs["Seed"],
                verify_limits=True,
            )
            node_tree.links.new(
                random_node.outputs["Value"], link.to_socket, verify_limits=True
            )
            node_tree.links.new(
                int_value_node.outputs["Integer"],
                random_node.inputs["ID"],
                verify_limits=True,
            )

            # # Remove the original link
            # node_tree.links.remove(link)

            return True

        except Exception as e:
            print(f"Error inserting Random Value node: {e}")
            return False

    def should_process_link(self, link: bpy.types.NodeLink) -> bool:
        """
        Check if a link should have a Random Value node inserted.

        Returns True for links from NodeGroupInput "seed" to node "seed" inputs,
        excluding existing auto-generated Random Value nodes.
        """
        from_socket: bpy.types.NodeSocket | None = getattr(link, "from_socket", None)
        to_socket: bpy.types.NodeSocket | None = getattr(link, "to_socket", None)

        if not (from_socket and to_socket):
            return False

        # from_socket checks
        if not (
            from_socket.node
            and isinstance(from_socket.node, bpy.types.NodeGroupInput)
            and from_socket.name.strip().lower() == "seed"
        ):
            return False

        # to_socket checks
        if (
            not to_socket.node
            or (
                isinstance(to_socket.node, bpy.types.FunctionNodeRandomValue)
                and to_socket.node.label == "Auto Random Seed"
            )
            or to_socket.name.strip().lower() != "seed"
        ):
            return False

        # # Check socket type compatibility
        # socket_type = getattr(to_socket, "type", None)
        # return socket_type in {"INT", "VALUE"}

        return True

    def should_process_tree(self, node_tree: bpy.types.NodeTree) -> bool:
        """Check if node tree has seed inputs that need processing."""
        try:
            assert node_tree.interface is not None, "Node tree has no interface"
            # Check if the node tree has a seed input
            for item in node_tree.interface.items_tree:
                if item.item_type == "SOCKET":
                    item = cast(bpy.types.NodeTreeInterfaceSocket, item)
                    if item.in_out == "INPUT" and item.name.strip().lower() == "seed":
                        return True
            return False
        except Exception as e:
            print(f"Error checking if tree should be processed: {e}")
            return False

    def process_tree(self, node_tree_name: str) -> None:
        """Process all eligible seed links in the node tree."""
        try:
            node_tree: bpy.types.NodeTree | None = bpy.data.node_groups.get(
                node_tree_name
            )
            if node_tree is None:
                print(f"Node tree '{node_tree_name}' not found")
                return

            # Find links that need Random Value nodes inserted
            links_to_process: list[bpy.types.NodeLink] = [
                link for link in node_tree.links[:] if self.should_process_link(link)
            ]

            # Find existing Random Value offsets
            existing_random_offsets: list[int] = list(
                set(
                    [
                        node.integer
                        for node in node_tree.nodes
                        if isinstance(node, bpy.types.FunctionNodeInputInt)
                        and node.label == "Auto Random Seed Offset"
                    ]
                )
            )

            new_offset = 0
            i = 0
            for link in links_to_process:
                while (
                    new_offset < len(existing_random_offsets)
                    and new_offset == existing_random_offsets[i]
                ):
                    new_offset += 1
                    i += 1
                self.process_link(node_tree, link, new_offset)
                new_offset += 1

        except Exception as e:
            print(f"Error processing node tree '{node_tree_name}': {e}")
