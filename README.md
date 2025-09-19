# Node Editor Tools

A Blender addon that automates common node editor tasks and improves workflow efficiency.

## Features

- **Automatic Seed Randomization**: Inserts Random Value nodes when seed inputs are connected
- **Single-Socket Group Cleanup**: Hides group input/output nodes with only one socket and labels them
- **Extensible Handler System**: Add custom node tree processors easily

## Installation

Refer to <https://extensions.blender.org/about/>

## Development

To add new handlers:

1. Create a handler file implementing `NodeTreeHandler`
2. Register it in `__init__.py`

The handler system supports extending functionality for different node tree types.
