from __future__ import annotations
from .seed_handler import register, unregister

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

if __name__ == "__main__":
    register()
