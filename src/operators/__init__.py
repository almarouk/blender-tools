"""
Operators for the node tree.
"""

from __future__ import annotations

__all__ = [
    "register",
    "unregister",
    "SplitMergeGroupInput",
    "HideRenameSingleOutputNode",
]

from bpy.utils import register_class, unregister_class

from .hide_node import HideResizeNode
from .split_group_input import SplitMergeGroupInput
from .rename_node import HideRenameSingleOutputNode
from .randomize_seed import RandomizeSeed

_classes = (
    HideResizeNode,
    SplitMergeGroupInput,
    HideRenameSingleOutputNode,
    RandomizeSeed,
)


def register():
    for cls in _classes:
        register_class(cls)


def unregister():
    for cls in reversed(_classes):
        unregister_class(cls)
