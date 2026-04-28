import numpy as np
import pytest

from k.core.state import State
from k.core.object import PhysicalObject
from k.core.subsystem import Subsystem


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


def test_subsystem_creation() -> None:
    subsys = Subsystem(name="test")
    assert subsys.name == "test"
    assert subsys.objects == []


def test_subsystem_add_object() -> None:
    subsys = Subsystem(name="test")
    state = make_state()
    obj = PhysicalObject(shape="box", state=state)
    subsys.add(obj)
    assert obj in subsys.objects


def test_subsystem_add_duplicate() -> None:
    subsys = Subsystem(name="test")
    state = make_state()
    obj = PhysicalObject(shape="box", state=state)
    subsys.add(obj)
    subsys.add(obj)
    assert subsys.objects.count(obj) == 1


def test_subsystem_remove_object() -> None:
    subsys = Subsystem(name="test")
    state = make_state()
    obj = PhysicalObject(shape="box", state=state)
    subsys.add(obj)
    subsys.remove(obj)
    assert obj not in subsys.objects


def test_subsystem_repr() -> None:
    subsys = Subsystem(name="test")
    assert "Subsystem" in repr(subsys)
