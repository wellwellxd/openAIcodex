"""roguelike.items.generator

generate_items(room_center: tuple[int, int], floor: int) -> list[Item]

Rules:
    • Rarity weights: common 0.7, rare 0.25, artifact 0.05
    • Tier = floor // 3 + 1  (cap at 5)
    • Item blueprints loaded from YAML / JSON in same package.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from .item import Item

_blueprints: list[dict[str, str]] | None = None


def _load_blueprints() -> list[dict[str, str]]:
    global _blueprints
    if _blueprints is None:
        path = Path(__file__).with_name("blueprints.json")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                _blueprints = json.load(f)
        else:
            _blueprints = [
                {"name": "Potion"},
                {"name": "Sword"},
                {"name": "Amulet"},
            ]
    return _blueprints


def generate_items(room_center: tuple[int, int], floor: int) -> list[Item]:
    blueprints = _load_blueprints()
    tier = min(floor // 3 + 1, 5)
    rarity_roll = random.random()
    if rarity_roll < 0.7:
        rarity = "common"
    elif rarity_roll < 0.95:
        rarity = "rare"
    else:
        rarity = "artifact"
    blueprint = random.choice(blueprints)
    return [Item(name=blueprint["name"], tier=tier, rarity=rarity)]
