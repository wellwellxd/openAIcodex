"""roguelike.render

Renderer draws the world to an ASCII console using python-tcod.
"""

from __future__ import annotations

import tcod

from roguelike.engine import World


class Renderer:
    """ASCII renderer using tcod console."""

    def __init__(self) -> None:
        self.context: tcod.context.Context | None = None
        self.console = tcod.Console(width=80, height=45, order="F")

    def _ensure_context(self) -> None:
        if self.context is None:
            tileset = tcod.tileset.load_tilesheet(
                "roguelike/data/tileset.png", 16, 16, tcod.tileset.CHARMAP_CP437
            )
            self.context = tcod.context.new(
                columns=80,
                rows=45,
                tileset=tileset,
                title="Roguelike",
                vsync=True,
            )

    def draw(self, world: World) -> None:
        """Render the map and player to the screen."""
        self._ensure_context()
        self.console.clear()
        for x in range(world.map.width):
            for y in range(world.map.height):
                tile = world.map.tiles[x][y]
                char = ord("#") if tile.blocked else ord(".")
                self.console.print(x=x, y=y, string=chr(char))
        px, py = world.player_pos
        self.console.print(x=px, y=py, string="@")
        assert self.context is not None
        self.context.present(self.console)
