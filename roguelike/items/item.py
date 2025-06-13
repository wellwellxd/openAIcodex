"""roguelike.items.item

Defines the Item dataclass used in the game world.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Item:
    """Basic item representation."""

    name: str
    tier: int
    rarity: str
