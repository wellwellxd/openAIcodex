"""roguelike.main

Bootstraps the game: load config, resume save if found, or start new world.
Keeps this file minimal so that Codex can focus on core logic elsewhere.
"""

from __future__ import annotations

import sys

from roguelike.engine import Engine
from roguelike.persistence import save_manager


def main() -> None:
    """Entry point for the roguelike."""
    world = save_manager.load()
    engine = Engine(world=world)
    engine.run()


if __name__ == "__main__":
    sys.exit(main())
