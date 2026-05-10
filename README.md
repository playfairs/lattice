# Lattice

A lightweight graph-based markdown/wiki editor inspired by Obsidian, built entirely in SETL with a reproducible Nix-based development environment.

## Features

- Create and edit markdown notes
- Link notes using [[wikilinks]]
- Tag notes using #tags
- Automatically build a graph of note relationships
- View backlinks and connections between notes
- Search notes by tag, title, and content
- Deterministic set-based logic
- Minimal, Unix-style design

## Architecture

### Core (SETL Only)

All application logic is implemented in SETL:

- **parser.setl** - Extracts [[wikilinks]] and #tags from markdown
- **graph.setl** - Manages note relationships using set-based operations
- **storage.setl** - File-per-note storage system
- **core.setl** - Main application logic and coordination
- **main.setl** - Entry point and command interface

### UI Layer (Minimal)

- **gui_bridge** - Shell script bridge between SETL core and GUI
- **gui.py** - Minimal Tkinter interface for rendering only

## Installation

### Using Nix (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd lattice

# Build the application
nix build

# Enter development environment
nix develop

# Run the application
./result/bin/lattice
```

### Development Setup

```bash
# Enter development shell
nix develop

# Run with GUI
lattice-run gui

# CLI usage
lattice-run create "My Note" "#tag Content with [[link]]"
lattice-run search "tag"
lattice-run backlinks "My Note"
```

## Usage

### GUI Mode

```bash
lattice gui
```

Launches the graphical interface with:
- Note list with search
- Markdown editor
- Graph visualization
- Backlinks viewer
- Tag management

### CLI Mode

```bash
# Create a note
lattice create "Title" "Content with [[link]] and #tag"

# Edit a note
lattice edit "Title" "Updated content"

# Get note content
lattice get "Title"

# Search notes
lattice search "query"

# Show backlinks
lattice backlinks "Title"

# Export graph data
lattice graph

# List notes by tag
lattice tags "tagname"

# List all notes
lattice list

# Delete a note
lattice delete "Title"
```

## Project Structure

```
lattice/
├── flake.nix              # Nix flake configuration
├── nix/
│   ├── buildPackages.nix  # Build dependencies
│   └── devShell.nix       # Development environment
├── src/
│   ├── setl/              # SETL core modules
│   │   ├── main.setl      # Entry point
│   │   ├── core.setl      # Core logic
│   │   ├── parser.setl    # Markdown parsing
│   │   ├── graph.setl     # Graph operations
│   │   └── storage.setl   # File storage
│   └── ui/                 # Minimal UI layer
│       ├── gui_bridge     # Shell script bridge
│       └── gui.py         # Python/Tkinter GUI
└── assets/                # Static assets
```

## Design Principles

- **SETL-only logic** - All core functionality in SETL
- **Set-based operations** - Leverage SETL's mathematical foundations
- **Deterministic behavior** - No dynamic runtime complexity
- **Minimal dependencies** - Only essential components
- **Unix philosophy** - Simple, composable tools
- **Reproducible builds** - Nix-based environment

## Wikilink Syntax

- `[[Note Title]]` - Link to another note
- `#tag` - Tag a note
- Links are automatically bidirectional
- Tags are collected globally for navigation

## Graph Operations

The system maintains:
- **Nodes** - Individual notes
- **Edges** - Wikilink relationships
- **Tags** - Many-to-many tag mappings
- **Backlinks** - Reverse link lookups

All graph operations use SETL set operations for optimal performance and correctness.

## Development

### Adding New Features

1. Implement core logic in appropriate SETL module
2. Add CLI commands in `main.setl`
3. Extend GUI bridge if needed
4. Update Nix configuration for new dependencies

### Testing

```bash
# Run tests in development environment
nix develop
lattice-run create "Test" "Content with [[link]]"
lattice-run search "Test"
lattice-run graph
```

## License

MIT License - see LICENSE file for details.