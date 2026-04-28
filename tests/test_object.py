import numpy as np
import pytest

from k.core.state import State, Wrench6T
from k.core.object import PhysicalObject


class DummyForce:
    def __init__(self, force: np.ndarray, point: np.ndarray) -> None:
        self.force = force
        self.point = point


class DummyTorque:
    def __init__(self, torque: np.ndarray) -> None:
        self.torque = torque


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


def test_object_creation() -> None:
    state = make_state()
    obj = PhysicalObject(shape="box", state=state)
    assert obj.shape == "box"
    assert obj.state is state
    assert isinstance(obj.id, str)


def test_object_custom_id() -> None:
    state = make_state()
    obj = PhysicalObject(shape="sphere", state=state, id="my_obj")
    assert obj.id == "my_obj"


def test_object_apply_force() -> None:
    state = make_state()
    obj = PhysicalObject(shape="box", state=state)
    force = np.array([0.0, 0.0, -9.8])
    point = np.array([0.0, 0.0, 0.0])
    obj.apply(DummyForce(force, point))
    assert len(obj.state.wrenches) == 1
    assert np.all(obj.state.wrenches[0][0][:3] == force)
    assert np.all(obj.state.wrenches[0][1] == point)


def test_object_apply_torque() -> None:
    state = make_state()
    obj = PhysicalObject(shape="box", state=state)
    torque = np.array([0.0, 0.0, 1.0])
    obj.apply(DummyTorque(torque))
    assert len(obj.state.wrenches) == 1
    assert np.all(obj.state.wrenches[0][0][3:] == torque)


def test_object_enable_domain() -> None:
    state = make_state()
    obj = PhysicalObject(shape="box", state=state)
    assert "thermodynamics" not in obj.state.enabled_domains
    obj.enable_domain("thermodynamics")
    assert "thermodynamics" in obj.state.enabled_domains


def test_object_disable_domain() -> None:
    state = make_state()
    obj = PhysicalObject(shape="box", state=state)
    obj.enable_domain("thermodynamics")
    obj.disable_domain("thermodynamics")
    assert "thermodynamics" not in obj.state.enabled_domains


def test_object_repr() -> None:
    state = make_state()
    obj = PhysicalObject(shape="box", state=state, id="test")
    assert "PhysicalObject" in repr(obj)
    assert "test" in repr(obj)
