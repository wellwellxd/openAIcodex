"""roguelike.map.tile

Defines the Tile dataclass representing a map tile.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Tile:
    """A single map tile."""

    blocked: bool
    block_sight: bool
    explored: bool = False
    light: int = 0
