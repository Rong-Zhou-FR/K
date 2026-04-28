import numpy as np
import pytest

from k.core.state import State, Vector3T, Wrench6T


def test_state_defaults() -> None:
    state = State(
        position=np.zeros(3),
        velocity=np.zeros(3),
        acceleration=np.zeros(3),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity=np.zeros(3),
        mass=1.0,
        inertia=np.eye(3),
    )
    assert state.temperature == 298.15
    assert state.heat_capacity == 1.0
    assert state.thermal_conductivity == 0.0
    assert state.charge == 0.0
    assert np.all(state.current == 0.0)
    assert np.all(state.magnetic_moment == 0.0)
    assert state.wrenches == []
    assert np.all(state.net_wrench == 0.0)
    assert state.heat_flows == []
    assert state.enabled_domains == {"mechanics"}


def test_state_custom_values() -> None:
    state = State(
        position=np.array([1.0, 2.0, 3.0]),
        velocity=np.zeros(3),
        acceleration=np.zeros(3),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity=np.zeros(3),
        mass=2.0,
        inertia=np.eye(3),
        temperature=310.0,
        enabled_domains={"mechanics", "thermodynamics"},
    )
    assert state.temperature == 310.0
    assert state.enabled_domains == {"mechanics", "thermodynamics"}


def test_state_wrench_types() -> None:
    state = State(
        position=np.zeros(3),
        velocity=np.zeros(3),
        acceleration=np.zeros(3),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity=np.zeros(3),
        mass=1.0,
        inertia=np.eye(3),
    )
    wrench = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], dtype=np.float64)
    point = np.array([0.0, 0.0, 0.0])
    state.wrenches.append((wrench, point))
    assert len(state.wrenches) == 1
    assert isinstance(state.wrenches[0][0], np.ndarray)
    assert state.wrenches[0][0].shape == (6,)
    assert state.wrenches[0][0].dtype == np.float64


def test_state_vector_types() -> None:
    pos = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    state = State(
        position=pos,
        velocity=np.zeros(3),
        acceleration=np.zeros(3),
        orientation=np.array([1.0, 0.0, 0.0, 0.0]),
        angular_velocity=np.zeros(3),
        mass=1.0,
        inertia=np.eye(3),
    )
    assert isinstance(state.position, np.ndarray)
    assert state.position.dtype == np.float64
