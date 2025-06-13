"""roguelike.engine

Central controller. No global state allowed outside this class.
"""

from __future__ import annotations

from typing import Optional
import time

from roguelike.map import generate_floor
from roguelike.render import Renderer
from roguelike.input import InputHandler
from roguelike.persistence import save_manager


class World:
    """Simple container for world state."""

    def __init__(self, seed: int, floor: int = 1) -> None:
        self.seed = seed
        self.floor = floor
        self.map = generate_floor(seed=seed, floor=floor)
        self.player_pos = list(self.map.up_pos)


class Engine:
    """Main game loop controller."""

    def __init__(self, world: Optional[World] = None) -> None:
        if world is None:
            world = World(seed=int(time.time()))
        self.world = world
        self.renderer = Renderer()
        self.input_handler = InputHandler()
        self.running = False

    def run(self) -> None:
        """Starts the blocking game loop until player quits."""
        self.running = True
        while self.running:
            self.renderer.draw(self.world)
            action = self.input_handler.get_action()
            if action == "QUIT":
                save_manager.save(self.world)
                break
            elif action in {"UP", "DOWN", "LEFT", "RIGHT"}:
                self._move_player(action)

    def _move_player(self, direction: str) -> None:
        dx, dy = 0, 0
        if direction == "UP":
            dy = -1
        elif direction == "DOWN":
            dy = 1
        elif direction == "LEFT":
            dx = -1
        elif direction == "RIGHT":
            dx = 1
        x, y = self.world.player_pos
        nx, ny = x + dx, y + dy
        if not self.world.map.tiles[nx][ny].blocked:
            self.world.player_pos = [nx, ny]

    def handle_player_death(self) -> None:
        """Show tombstone, delete save, return to menu."""
        save_manager.delete()
        self.running = False
