from __future__ import annotations

import numpy as np
from k.viz.diagrams.force import ForceDiagram
from k.core.state import State
from k.core.object import PhysicalObject


def test_force_diagram_init() -> None:
    fd = ForceDiagram()
    assert fd.scale == 0.1
    assert fd.color == "red"


def test_force_diagram_custom() -> None:
    fd = ForceDiagram(scale=0.5, color="blue")
    assert fd.scale == 0.5
    assert fd.color == "blue"


def test_force_diagram_draw_2d_no_forces() -> None:
    import matplotlib.pyplot as plt

    fd = ForceDiagram()
    state = State(
        position=np.array([0, 0, 0], dtype=np.float64),
        velocity=np.zeros(3, dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )
    obj = PhysicalObject(shape="point", state=state, id="obj1")
    fig, ax = plt.subplots()
    fd.draw_on_object_2d(obj, ax)
    plt.close(fig)


def test_force_diagram_draw_2d_with_forces() -> None:
    import matplotlib.pyplot as plt

    fd = ForceDiagram(scale=0.1)
    state = State(
        position=np.array([0, 0, 0], dtype=np.float64),
        velocity=np.zeros(3, dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )
    wrench = np.zeros(6, dtype=np.float64)
    wrench[:3] = [10, 5, 0]
    state.wrenches.append((wrench, state.position.copy()))
    obj = PhysicalObject(shape="point", state=state, id="obj1")
    fig, ax = plt.subplots()
    fd.draw_on_object_2d(obj, ax)
    plt.close(fig)


def test_force_diagram_draw_2d_with_point() -> None:
    import matplotlib.pyplot as plt

    fd = ForceDiagram()
    state = State(
        position=np.array([0, 0, 0], dtype=np.float64),
        velocity=np.zeros(3, dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )
    wrench = np.zeros(6, dtype=np.float64)
    wrench[:3] = [10, 0, 0]
    state.wrenches.append((wrench, np.array([1, 1, 0], dtype=np.float64)))
    obj = PhysicalObject(shape="point", state=state, id="obj1")
    fig, ax = plt.subplots()
    fd.draw_on_object_2d(obj, ax)
    plt.close(fig)
