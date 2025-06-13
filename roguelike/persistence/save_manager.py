"""roguelike.persistence.save_manager

Single-file save system (overwrite, delete-on-death).

Public methods:
    save(world)   # → None
    load()        # → Optional[World]
    delete()      # → None
Path must follow platformdirs.user_data_dir("Roguelike", "")
Use orjson with OPT_SERIALIZE_NUMPY. Tiles may be zstd-compressed.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import orjson
from platformdirs import user_data_dir

from roguelike.engine import World

SAVE_PATH = Path(user_data_dir("Roguelike", "")) / "save.json"


def save(world: World) -> None:
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "seed": world.seed,
        "floor": world.floor,
        "player_pos": world.player_pos,
    }
    with open(SAVE_PATH, "wb") as f:
        f.write(orjson.dumps(data))


def load() -> Optional[World]:
    if not SAVE_PATH.exists():
        return None
    with open(SAVE_PATH, "rb") as f:
        data = orjson.loads(f.read())
    world = World(seed=data["seed"], floor=data["floor"])
    world.player_pos = list(data.get("player_pos", world.player_pos))
    return world


def delete() -> None:
    if SAVE_PATH.exists():
        SAVE_PATH.unlink()
