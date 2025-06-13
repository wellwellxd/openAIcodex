"""roguelike.map.generator

Expose `generate_floor(seed: int, floor: int) -> Map`.
Uses recursive BSP. Parameters are pulled from config.yaml.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

from .tile import Tile


@dataclass
class Rect:
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def center(self) -> tuple[int, int]:
        return ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1


def load_config() -> dict[str, float]:
    path = Path(__file__).resolve().parents[1] / "data" / "config.yaml"
    cfg: dict[str, float] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                try:
                    cfg[key.strip()] = int(value.strip())
                except ValueError:
                    cfg[key.strip()] = float(value.strip())
    return cfg


class Map:
    """Game map consisting of tiles and rooms."""

    def __init__(self, width: int, height: int, tiles: list[list[Tile]]) -> None:
        self.width = width
        self.height = height
        self.tiles = tiles
        self.rooms: list[Rect] = []
        self.up_pos: tuple[int, int] = (1, 1)
        self.down_pos: tuple[int, int] = (width - 2, height - 2)


def generate_floor(seed: int, floor: int) -> Map:
    cfg = load_config()
    random.seed(seed + floor)
    width = int(cfg.get("map_width", 80))
    height = int(cfg.get("map_height", 45))
    tiles = [[Tile(blocked=True, block_sight=True) for _ in range(height)] for _ in range(width)]
    game_map = Map(width=width, height=height, tiles=tiles)

    room1 = Rect(1, 1, width // 2 - 1, height // 2 - 1)
    room2 = Rect(width // 2 + 1, height // 2 + 1, width - 2, height - 2)
    game_map.rooms.extend([room1, room2])

    for room in game_map.rooms:
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                game_map.tiles[x][y] = Tile(blocked=False, block_sight=False)

    game_map.up_pos = room1.center
    game_map.down_pos = room2.center
    return game_map
