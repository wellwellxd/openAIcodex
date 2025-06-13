"""roguelike.fov.lighting

FOVSystem.update(world) -> mutates tile.light & tile.explored.

Implementation rules:
    * Use tcod.map.compute_fov with FOV_RESTRICTIVE.
    * Support additional light sources world.lights (pos, radius, strength).
"""

from __future__ import annotations

import tcod

from roguelike.engine import World


class FOVSystem:
    """Handles field-of-view and lighting calculations."""

    def __init__(self) -> None:
        self.fov_map: tcod.map.Map | None = None

    def initialize(self, world: World) -> None:
        self.fov_map = tcod.map.Map(world.map.width, world.map.height)
        for x in range(world.map.width):
            for y in range(world.map.height):
                tile = world.map.tiles[x][y]
                self.fov_map.walkable[x, y] = not tile.blocked
                self.fov_map.transparent[x, y] = not tile.block_sight

    def update(self, world: World, position: tuple[int, int]) -> None:
        if self.fov_map is None:
            self.initialize(world)
        assert self.fov_map is not None
        self.fov_map.compute_fov(*position, radius=8, algorithm=tcod.FOV_RESTRICTIVE)
        for x in range(world.map.width):
            for y in range(world.map.height):
                visible = self.fov_map.fov[x, y]
                tile = world.map.tiles[x][y]
                tile.explored |= visible
                tile.light = 255 if visible else 0
