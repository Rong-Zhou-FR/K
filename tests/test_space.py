import numpy as np
import pytest

from k.core.state import State
from k.core.object import PhysicalObject
from k.core.space import Space


def make_state() -> State:
    return State(
        position=np.zeros(3),
        velocity=np.zeros(3),
        acceleration=np.zeros(3),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity=np.zeros(3),
        mass=1.0,
        inertia=np.eye(3),
    )


def test_space_creation() -> None:
    space = Space(dimensions=3)
    assert space.dimensions == 3
    assert space.objects == {}
    assert space.enabled_domains == {"mechanics"}


def test_space_2d() -> None:
    space = Space(dimensions=2)
    assert space.dimensions == 2


def test_space_invalid_dimensions() -> None:
    with pytest.raises(ValueError):
        Space(dimensions=4)


def test_space_add_object() -> None:
    space = Space()
    state = make_state()
    obj = PhysicalObject(shape="box", state=state, id="box1")
    space.add(obj)
    assert "box1" in space.objects
    assert space.objects["box1"] is obj


def test_space_add_duplicate_id() -> None:
    space = Space()
    state = make_state()
    obj1 = PhysicalObject(shape="box", state=state, id="same_id")
    obj2 = PhysicalObject(shape="sphere", state=make_state(), id="same_id")
    space.add(obj1)
    with pytest.raises(ValueError):
        space.add(obj2)


def test_space_remove_object() -> None:
    space = Space()
    state = make_state()
    obj = PhysicalObject(shape="box", state=state, id="box1")
    space.add(obj)
    space.remove("box1")
    assert "box1" not in space.objects


def test_space_enable_domain() -> None:
    space = Space()
    state = make_state()
    obj = PhysicalObject(shape="box", state=state, id="box1")
    space.add(obj)
    space.enable_domain("thermodynamics")
    assert "thermodynamics" in space.enabled_domains
    assert "thermodynamics" in obj.state.enabled_domains


def test_space_disable_domain() -> None:
    space = Space()
    state = make_state()
    obj = PhysicalObject(shape="box", state=state, id="box1")
    space.add(obj)
    space.enable_domain("thermodynamics")
    space.disable_domain("thermodynamics")
    assert "thermodynamics" not in space.enabled_domains
    assert "thermodynamics" not in obj.state.enabled_domains


def test_space_repr() -> None:
    space = Space()
    assert "Space" in repr(space)
