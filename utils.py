# Code adapted from: https://blender.stackexchange.com/a/252856/248376
"""Utilities for calculating node socket positions in Blender's node editor."""

import bpy

X_OFFSET = -1.0
Y_TOP = -34.0
Y_BOTTOM = 16.0
Y_OFFSET = 22.0

# 2 offsets
VEC_BOTTOM = 28.0
VEC_TOP = 32.0


def is_hidden(socket: bpy.types.NodeSocket) -> bool:
    """Check if a node socket is hidden or disabled."""
    return socket.hide or not socket.enabled


def is_tall(node: bpy.types.Node, socket: bpy.types.NodeSocket) -> bool:
    """Check if a socket should use tall spacing (vector sockets with visible values)."""
    if socket.type != "VECTOR":
        return False
    if socket.hide_value:
        return False
    if socket.is_linked:
        return False
    if node.type == "BSDF_PRINCIPLED" and socket.identifier == "Subsurface Radius":
        return False  # an exception confirms a rule?
    return True


def get_node_socket_location(
    node: bpy.types.Node, socket_key: str, is_input: bool
) -> tuple[float, float] | None:
    """Calculate the screen position of a node socket.
    
    Args:
        node: The Blender node containing the socket
        socket_key: Name/key of the socket to locate
        is_input: True for input socket, False for output socket
        
    Returns:
        (x, y) coordinates of the socket, or None if node/socket is hidden
    """
    try:
        if node.hide:
            return None
        socket_key = socket_key.strip().lower()

        if not is_input:
            x = node.location.x + node.dimensions.x + X_OFFSET
            y = node.location.y + Y_TOP
            for i, (key, socket) in enumerate(node.outputs.items()):
                key = key.strip().lower()
                if is_hidden(socket):
                    if key == socket_key:
                        return None
                    continue
                if key == socket_key:
                    return x, y
                y -= Y_OFFSET
        else:
            x = node.location.x
            y = node.location.y - node.dimensions.y + Y_BOTTOM
            for i, (key, socket) in enumerate(reversed(node.inputs.items())):
                key = key.strip().lower()
                if is_hidden(socket):
                    if key == socket_key:
                        return None
                    continue
                tall = is_tall(node, socket)
                y += VEC_BOTTOM * tall
                if key == socket_key:
                    return x, y
                y += Y_OFFSET + VEC_TOP * tall
    except Exception as e:
        print(f"Error getting socket location: {e}")
        return None
