# CLAUDE.md - AI Assistant Guide

This document provides essential context for AI assistants working with this codebase.

## Project Overview

**openAIcodex** is an ASCII roguelike dungeon-crawler game built in Python. Players navigate procedurally-generated dungeon floors, collect items, and explore a world rendered in ASCII characters. The project demonstrates clean game architecture with proper separation of concerns.

## Tech Stack

- **Language**: Python 3.11
- **Rendering**: tcod (ASCII/Unicode graphics)
- **Input**: pygame (keyboard events)
- **Serialization**: orjson (save files)
- **Package Manager**: Poetry
- **Linting**: Ruff
- **Type Checking**: MyPy
- **Testing**: Pytest
- **Packaging**: PyInstaller

## Project Structure

```
/
├── .github/workflows/ci.yaml    # CI/CD pipeline
├── roguelike/                   # Main game package
│   ├── main.py                  # Entry point - bootstrap and config loading
│   ├── engine.py                # Core game loop and World state container
│   ├── render.py                # ASCII rendering (tcod)
│   ├── input.py                 # Keyboard input handling (pygame)
│   ├── data/
│   │   ├── config.yaml          # Game configuration parameters
│   │   └── tileset.png          # Character tileset
│   ├── map/
│   │   ├── generator.py         # BSP-based procedural map generation
│   │   └── tile.py              # Tile dataclass
│   ├── fov/
│   │   └── lighting.py          # Field-of-view calculations
│   ├── items/
│   │   ├── item.py              # Item dataclass
│   │   └── generator.py         # Procedural item generation
│   ├── persistence/
│   │   └── save_manager.py      # Save/load system
│   ├── util/
│   │   └── type_defs.py         # Type aliases (Position)
│   └── tests/
│       └── test_map.py          # Map generation tests
├── hello_world.py               # Simple example script
└── README.md
```

## Development Commands

```bash
# Install dependencies
poetry install

# Run linter
poetry run ruff .

# Run type checker
poetry run mypy roguelike

# Run tests
poetry run pytest -q

# Build standalone executable
poetry run pyinstaller --onefile -n roguelike -m roguelike.main

# Run the game (development)
poetry run python -m roguelike.main
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yaml`) runs on:
- Push to `main` branch
- All pull requests

Pipeline steps: Install dependencies -> Lint (ruff + mypy) -> Test (pytest) -> Build (pyinstaller)

## Code Conventions

### Style Guidelines

1. **Type Hints**: Full PEP 484 type annotations are required throughout
2. **Imports**: Use `from __future__ import annotations` at the top of every module
3. **Docstrings**: Module-level docstrings explaining purpose and design decisions
4. **Data Structures**: Use `@dataclass` for data containers (Tile, Item, etc.)

### Architecture Principles

1. **No Global State**: All world state is contained in `Engine.world` class
2. **Separation of Concerns**: Each package handles one responsibility:
   - `map/` - Map generation
   - `fov/` - Visibility calculations
   - `items/` - Item system
   - `persistence/` - Save/load
   - `render.py` - Display
   - `input.py` - User input
3. **Package Exports**: Each `__init__.py` exports the public API

### Naming Conventions

- Classes: `PascalCase` (e.g., `World`, `Engine`, `Tile`)
- Functions/Methods: `snake_case` (e.g., `generate_floor`, `_move_player`)
- Private methods: Prefix with underscore (e.g., `_move_player`)
- Type aliases: `PascalCase` in `util/type_defs.py` (e.g., `Position`)
- Constants in config: `snake_case` (e.g., `fov_radius`, `map_width`)

## Configuration

Game parameters are stored in `roguelike/data/config.yaml`:
- `fov_radius: 8` - Player vision range
- `map_width: 80` - Console width
- `map_height: 45` - Console height
- `treasure_room_chance: 0.05` - 5% treasure room probability

## Game Architecture

### Core Loop (engine.py)
1. Render world to screen
2. Wait for player input
3. Validate and apply movement
4. Save on quit, delete on death

### Map Generation (map/generator.py)
- Recursive Binary Space Partition (BSP) algorithm
- Seeded for reproducible dungeons
- Supports multiple floor levels

### Item System (items/)
- Procedural rarity: 70% common, 25% rare, 5% artifact
- Tier scales with floor level (`floor // 3 + 1`)

### Save System (persistence/)
- Single-file saves using orjson
- Stores: seed, floor, player position
- Platform-specific data directory via `platformdirs`
- Delete-on-death permadeath mechanic

### Controls
- Arrow keys or vi-style (h/j/k/l)
- ESC or window close to quit

## Testing Guidelines

Tests are located in `roguelike/tests/`. Current test coverage:
- `test_map.py` - Validates map generation creates 2+ rooms with distinct stairs

When adding tests:
1. Place in `roguelike/tests/`
2. Prefix test files with `test_`
3. Use descriptive test names: `test_<what>_<expected_behavior>`
4. Include type hints on test functions

## Common Tasks for AI Assistants

### Adding a New Feature
1. Identify the appropriate package/module
2. Follow existing patterns for dataclasses and type hints
3. Add tests for new functionality
4. Run `poetry run ruff .` and `poetry run mypy roguelike` before committing

### Modifying Game Mechanics
1. Engine logic lives in `roguelike/engine.py`
2. Map generation in `roguelike/map/generator.py`
3. Update `config.yaml` for tunable parameters

### Debugging
1. Entry point is `roguelike/main.py`
2. Game state is encapsulated in `Engine.world`
3. Save files are stored via `platformdirs` (check `~/.local/share/Roguelike/` on Linux)

## Important Notes

- Always run linting and type checking before creating commits
- Keep modules focused on single responsibilities
- Prefer editing existing files over creating new ones
- Configuration changes go in `config.yaml`, not hardcoded values
