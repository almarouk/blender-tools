# Node Editor Tools

*Automation helpers that keep Blender's node editor tidy, readable, and fast to iterate.*

[![Blender 4.2+](https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender)](https://www.blender.org/download/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

Blender's node editor gets cluttered fast. Node Editor Tools ships with a growing toolbox of handlers and operators that automate the repetitive bits—naming, splitting, hiding, wiring—so you can stay focused on the look of your graph instead of its housekeeping.

## Table of Contents

- [Node Editor Tools](#node-editor-tools)
  - [Table of Contents](#table-of-contents)
  - [Highlights](#highlights)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [From a packaged release](#from-a-packaged-release)
    - [Build the archive yourself](#build-the-archive-yourself)
  - [Getting Started](#getting-started)
  - [Usage](#usage)
    - [Automatic Handlers](#automatic-handlers)
    - [Split \& Merge Group Inputs](#split--merge-group-inputs)
    - [Hide \& Resize Toggle](#hide--resize-toggle)
  - [Extending the Add-on](#extending-the-add-on)
  - [Development Workflow](#development-workflow)
  - [Troubleshooting](#troubleshooting)
  - [License](#license)

## Highlights

- **Automatic Seed Randomization** – Injects hidden Random Value chains when a linked socket is named "Seed", ensuring every instance gets a unique offset.
- **Single-Socket Group Cleanup** – Detects lonely group input/output sockets, collapses the node, and labels it after the exposed socket.
- **Split & Merge Group Inputs** – Context menu operator that spawns one Group Input per link, destination node, or source socket; also merges them back together on demand.
- **Hide & Resize Toggle** – Double-press `H` to shrink hidden nodes (or restore their default width) without touching visibility flags.
- **Extensible Handler System** – Drop in your own `NodeTreeHandler` to react to node tree events alongside the built-ins.

## Requirements

- Blender **4.2.0 or newer** (matches the `blender_manifest.toml` minimum).
- Access to the Shader, Geometry, or Compositor node editors.
- Permission to install add-ons on your Blender installation.

## Installation

### From a packaged release

1. Download the latest `.zip` build (either from a release or using the build helper below).
2. In Blender, open **Edit ▸ Preferences ▸ Add-ons**.
3. Click **Install…**, choose the downloaded archive, and enable **Node Editor Tools**.

### Build the archive yourself

1. Copy `.env.example` to `.env` and set `BLENDER_PATH` to your Blender executable.
2. Ensure Python 3.11+ is on your PATH.
3. Run:

   ```powershell
   python build.py validate
   python build.py build
   ```

   The packaged add-on will appear in the `build/` directory.

4. (Optional) Install straight into Blender for rapid iteration:

   ```powershell
   python build.py install
   ```

## Getting Started

1. Enable **Node Editor Tools** in **Edit ▸ Preferences ▸ Add-ons**.
2. Open any node editor (Shader, Geometry, Compositor, etc.).
3. Start creating or editing a node group—handlers run automatically in the background, and operators show up in context menus and shortcuts.

## Usage

### Automatic Handlers

- **Seed Randomizer** activates when a group exposes a socket named "Seed" that is linked in the node editor. A hidden Random Value node (plus an Integer offset) is inserted and wired for you so every consumer receives a unique seed.
- **Single Socket Cleanup** activates on node tree changes. If a node exposes exactly one visible socket, it collapses the node, hides it, and renames it to match the socket label.

### Split & Merge Group Inputs

1. Select one or more Group Input nodes.
2. Right-click to open the context menu and pick **Split/Merge**.
3. Choose a mode in the popup:
   - **Link** – creates one hidden Group Input per outgoing link.
   - **Destination Node** – clusters connections per receiving node.
   - **Source Socket** – keeps one node per exposed socket.
   - **Merge All** – collapses multiple inputs back into a single node.

Each generated Group Input is hidden and labelled for quick inspection. Run the operator again at any time to return to a compact setup.

Toggle **Process Individually** in the popup if you prefer each selected Group Input to be split on its own. Leave it disabled to merge all selected nodes before splitting—ideal for building a unified input layout in one pass.

### Hide & Resize Toggle

- Double-tap `H` in the node editor (with the add-on enabled) to run **Hide and Resize Nodes**.
- Hidden nodes shrink to their minimum width, keeping them out of the way while still accessible.
- Visible nodes temporarily expand back to their default width, aiding readability.

## Extending the Add-on

- Handlers live in `src/node_tree_handlers/`. Implement the `NodeTreeHandler` protocol and register your class inside `src/node_tree_handlers/__init__.py` to add new automation.
- Operators and menus reside under `src/operators/` and `src/interface/`; they register automatically via their respective `__init__.py` files.
- Utility helpers shared between handlers/operators live in `src/utils/`.

## Development Workflow

- The project uses [Blender's extension tooling](https://projects.blender.org/extensions) via `build.py`.
- `python build.py validate` validates the manifest without building the package.
- `python build.py build` packages the add-on into `build/blender_tools.zip`.
- `python build.py install` installs directly into the Blender specified by `BLENDER_PATH`—handy for testing changes quickly.

## Troubleshooting

- Re-run `python build.py validate` if Blender refuses to install the archive—errors will reference missing metadata or incompatible files.
- Ensure the *Node Editor* context is active when testing shortcuts; handlers only process events for supported node spaces.
- Delete the add-on folder from your Blender configuration and reinstall if upgrades behave unexpectedly.

## License

Distributed under the terms of the [GPLv3](LICENSE).
