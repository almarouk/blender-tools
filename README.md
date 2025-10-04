# Node Editor Tools

Quality-of-life automation for Blender's node editor. The addon ships with a set of handlers and operators that keep node trees tidy, automate repetitive wiring, and expose context-sensitive tools.

## Features at a Glance

- **Automatic Seed Randomization** – Inserts hidden Random Value chains whenever a "Seed" socket is linked so every instance gets a unique offset.
- **Single-Socket Group Cleanup** – Detects lonely group input/output sockets, hides the node, and labels it after the exposed socket.
- **Group Input Split & Merge** – Context menu operator that spawns one Group Input per link, destination, or source socket—or merges everything back together.
- **Hide & Resize Toggle** – Double-press `H` to shrink hidden nodes (or restore their default width) without touching the node visibility.
- **Extensible Handler System** – Drop in your own `NodeTreeHandler` to react to node tree events alongside the built-in processors.

## Installation

1. Download or build the add-on `.zip` (see Development below for the build helper).
2. In Blender, go to **Edit ▸ Preferences ▸ Add-ons** and choose **Install**.
3. Select the downloaded archive and enable **Node Editor Tools**.

## Usage

### Automatic handlers

- **Seed Randomizer** fires when a group exposes a socket named "Seed" and that socket is linked in the node editor. A hidden Random Value node (plus an Integer offset) is inserted and wired for you.
- **Single Socket Cleanup** scans all Group Input and Group Output nodes and collapses any with exactly one visible socket, keeping your graphs compact.

### Split & merge group inputs

1. Select one or more Group Input nodes in the node editor.
2. Open the context menu (right-click) and pick **Split/Merge**.
3. Choose a mode in the popup:
   - **Link** creates one hidden Group Input per outgoing link.
   - **Destination Node** clusters connections per receiving node.
   - **Source Socket** keeps one node per exposed socket.
   - **Merge All** collapses multiple inputs back into a single node.

### Hide & resize toggle

- Double-press `H` in the node editor (while the addon is enabled) to run **Hide and Resize Nodes**.
- Hidden nodes shrink to their minimum width, while visible ones temporarily expand back to their default width.

## Development

- Use `python build.py validate|build|install` to drive Blender's extension tooling. Copy `.env.example` to `.env` and set `BLENDER_PATH` to your Blender executable first.
- Handlers live under `src/node_tree_handlers/`. Implement the `NodeTreeHandler` protocol and register the class inside `src/node_tree_handlers/__init__.py` to add new automation.
- Operators and menus are in `src/operators/` and `src/interface/`; they register automatically via `__init__.py`.
