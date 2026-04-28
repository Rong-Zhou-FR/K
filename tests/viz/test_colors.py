from __future__ import annotations

from k.viz.colors import DOMAIN_COLORS, get_domain_color, get_object_color
from k.core.state import State
from k.core.object import PhysicalObject
import numpy as np


def test_domain_colors_keys() -> None:
    assert "mechanics" in DOMAIN_COLORS
    assert "thermodynamics" in DOMAIN_COLORS
    assert "electromagnetism" in DOMAIN_COLORS
    assert "optics" in DOMAIN_COLORS
    assert "fluid" in DOMAIN_COLORS


def test_get_domain_color_known() -> None:
    assert get_domain_color("mechanics") == "#1f77b4"
    assert get_domain_color("optics") == "#d62728"


def test_get_domain_color_unknown() -> None:
    assert get_domain_color("unknown") == "#333333"


def test_get_object_color() -> None:
    state = State(
        position=np.array([0, 0, 0], dtype=np.float64),
        velocity=np.zeros(3, dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
        enabled_domains={"optics"},
    )
    obj = PhysicalObject(shape="sphere", state=state, id="test")
    color = get_object_color(obj)
    assert color == "#d62728"


def test_get_object_color_default() -> None:
    state = State(
        position=np.array([0, 0, 0], dtype=np.float64),
        velocity=np.zeros(3, dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
        enabled_domains=set(),
    )
    obj = PhysicalObject(shape="sphere", state=state, id="test")
    color = get_object_color(obj)
    assert color == "#333333"
