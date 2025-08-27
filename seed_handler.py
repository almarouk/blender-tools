import bpy
from bpy.app.handlers import persistent
from functools import partial

bl_info = {
    "name": "Seed Randomizer for Geometry Nodes",
    "author": "almarouk",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "Geometry Nodes",
    "description": "Automatically inserts Random Value nodes when Seed inputs are linked",
    "warning": "",
    "doc_url": "",
    "category": "Node",
}

# Global state to track handler registration
_handler_registered: bool = False


def process_link(
    node_tree: bpy.types.GeometryNodeTree, link: bpy.types.NodeLink, new_offset: int
) -> bool:
    try:
        to_node = link.to_socket.node

        # print(f"Inserting Random Value node between '{from_node.name}' and '{to_node.name}'")

        # Create Random Value node
        random_node: bpy.types.FunctionNodeRandomValue = node_tree.nodes.new(
            type="FunctionNodeRandomValue"
        )
        random_node.location = (to_node.location.x - random_node.bl_width_default - 50, to_node.location.y)
        random_node.label = "Auto Random Seed"
        random_node.data_type = "INT"

        # Set default range for integer random values
        socket: bpy.types.NodeSocketInt = random_node.inputs["Min"]
        socket.default_value = 0
        socket: bpy.types.NodeSocketInt = random_node.inputs["Max"]
        socket.default_value = 1000000

        # Add an Integer Value Node
        int_value_node: bpy.types.FunctionNodeInputInt = node_tree.nodes.new(
            type="FunctionNodeInputInt"
        )
        int_value_node.location = (random_node.location.x - int_value_node.bl_width_default - 50, random_node.location.y)
        int_value_node.label = "Auto Random Seed Offset"
        int_value_node.integer = new_offset

        # Create new links through the Random Value node
        node_tree.links.new(link.from_socket, random_node.inputs["Seed"], verify_limits=True)
        node_tree.links.new(random_node.outputs["Value"], link.to_socket, verify_limits=True)
        node_tree.links.new(int_value_node.outputs["Integer"], random_node.inputs["ID"], verify_limits=True)

        # # Remove the original link
        # node_tree.links.remove(link)

        return True

    except Exception as e:
        print(f"Error inserting Random Value node: {e}")
        return False


def should_process_link(link: bpy.types.NodeLink) -> bool:
    """Fast check if a link should be processed for seed insertion"""
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


@persistent
def check_seed_links(scene: bpy.types.Scene, depsgraph: bpy.types.Depsgraph) -> None:
    """Handler to check for new seed links and insert Random Value nodes"""

    # bpy.ops.node.select_all(action='DESELECT')

    try:
        # Get updated geometry node trees from depsgraph for better performance
        updated_node_trees: set[bpy.types.GeometryNodeTree] = set()

        for update in depsgraph.updates[:]:
            update_id: bpy.types.ID | None = getattr(update, "id", None)
            if not update_id:
                continue

            # Check if the updated object is a geometry node tree
            if update_id and isinstance(update_id, bpy.types.GeometryNodeTree):
                update_id: bpy.types.GeometryNodeTree
                for item in update_id.interface.items_tree:
                    if item.item_type == "SOCKET":
                        item: bpy.types.NodeTreeInterfaceSocket
                        if (
                            item.in_out == "INPUT"
                            and item.name.strip().lower() == "seed"
                        ):
                            updated_node_trees.add(update_id)
                            break

        # Process only the updated geometry node trees
        for node_tree in updated_node_trees:
            bpy.app.timers.register(partial(process_node_tree_links, node_tree.name), first_interval=1)
            # process_node_tree_links(node_tree)

    except Exception as e:
        print(f"Error in seed link handler: {e}")


def process_node_tree_links(node_tree_name: str) -> None:
    """Process links in a specific node tree for seed connections"""

    try:
        node_tree: bpy.types.GeometryNodeTree | None = bpy.data.node_groups.get(node_tree_name)
        if not node_tree:
            print(f"Node tree '{node_tree_name}' not found")
            return

        # Find links that need Random Value nodes inserted
        links_to_process: list[bpy.types.NodeLink] = [
            link for link in node_tree.links[:] if should_process_link(link)
        ]

        # Find existing Random Value offsets
        existing_random_offsets: list[int] = list(set(
            [
                node.integer
                for node in node_tree.nodes
                if isinstance(node, bpy.types.FunctionNodeInputInt)
                and node.label == "Auto Random Seed Offset"
            ]
        ))

        new_offset = 0
        i = 0
        for link in links_to_process:
            while new_offset < len(existing_random_offsets) and new_offset == existing_random_offsets[i]:
                new_offset += 1
                i += 1
            process_link(node_tree, link, new_offset)
            new_offset += 1

    except Exception as e:
        print(f"Error processing node tree '{node_tree.name}': {e}")


def register() -> None:
    """Register the handler (enabled by default)"""
    global _handler_registered

    if not _handler_registered:
        bpy.app.handlers.depsgraph_update_post.append(check_seed_links)
        _handler_registered = True
        print("Seed randomizer handler registered")


def unregister() -> None:
    """Unregister the handler"""
    global _handler_registered, _last_update_frame

    if _handler_registered:
        if check_seed_links in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(check_seed_links)
        _handler_registered = False
        _last_update_frame = -1
        print("Seed randomizer handler unregistered")


if __name__ == "__main__":
    register()
