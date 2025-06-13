"""Smoke-test Map generation guarantees at least 2 rooms and stairs."""

from roguelike.map.generator import generate_floor


def test_basic_floor() -> None:
    m = generate_floor(seed=123, floor=1)
    assert len(m.rooms) >= 2
    assert m.up_pos != m.down_pos
