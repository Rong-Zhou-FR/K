from __future__ import annotations

import numpy as np
from k.viz.diagrams.optical import OpticalDiagram
from k.core.state import State
from k.core.object import PhysicalObject
from k.core.space import Space


def test_optical_diagram_init() -> None:
    od = OpticalDiagram()
    assert od.ray_color == "yellow"
    assert od.lens_color == "blue"
    assert od.mirror_color == "gray"


def test_optical_diagram_custom() -> None:
    od = OpticalDiagram(ray_color="green", lens_color="red", mirror_color="black")
    assert od.ray_color == "green"
    assert od.lens_color == "red"
    assert od.mirror_color == "black"


def test_optical_diagram_draw_rays_2d_empty() -> None:
    import matplotlib.pyplot as plt

    od = OpticalDiagram()
    space = Space(dimensions=2)
    fig, ax = plt.subplots()
    od.draw_rays_2d(space, ax)
    plt.close(fig)


def test_optical_diagram_draw_rays_2d_with_ray() -> None:
    import matplotlib.pyplot as plt

    od = OpticalDiagram()
    state = State(
        position=np.array([0, 0, 0], dtype=np.float64),
        velocity=np.zeros(3, dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )
    obj = PhysicalObject(shape="ray", state=state, id="ray1")
    obj.path = [(0, 0, 0), (1, 1, 0), (2, 0, 0)]
    space = Space(dimensions=2)
    space.add(obj)
    fig, ax = plt.subplots()
    od.draw_rays_2d(space, ax)
    plt.close(fig)


def test_optical_diagram_draw_elements_2d() -> None:
    import matplotlib.pyplot as plt

    od = OpticalDiagram()
    state = State(
        position=np.array([0, 0, 0], dtype=np.float64),
        velocity=np.zeros(3, dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )
    lens = PhysicalObject(shape="lens", state=state, id="lens1")
    mirror_state = State(
        position=np.array([5, 0, 0], dtype=np.float64),
        velocity=np.zeros(3, dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )
    mirror = PhysicalObject(shape="mirror", state=mirror_state, id="mirror1")
    space = Space(dimensions=2)
    space.add(lens)
    space.add(mirror)
    fig, ax = plt.subplots()
    od.draw_optical_elements_2d(space, ax)
    plt.close(fig)
