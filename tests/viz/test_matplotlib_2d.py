from __future__ import annotations

import numpy as np
from k.viz.matplotlib_2d import Matplotlib2D
from k.viz.base import RenderConfig
from k.core.state import State
from k.core.object import PhysicalObject
from k.core.space import Space


def test_matplotlib_2d_dimensions() -> None:
    renderer = Matplotlib2D()
    assert renderer.dimensions == 2


def test_matplotlib_2d_render_empty_space() -> None:
    renderer = Matplotlib2D()
    space = Space(dimensions=2)
    fig = renderer.render(space)
    assert fig is not None
    renderer.close()


def test_matplotlib_2d_render_with_object() -> None:
    renderer = Matplotlib2D()
    state = State(
        position=np.array([1, 2, 0], dtype=np.float64),
        velocity=np.zeros(3, dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )
    obj = PhysicalObject(shape="sphere", state=state, id="obj1")
    space = Space(dimensions=2)
    space.add(obj)
    fig = renderer.render(space)
    assert fig is not None
    renderer.close()


def test_matplotlib_2d_render_with_force() -> None:
    renderer = Matplotlib2D()
    state = State(
        position=np.array([0, 0, 0], dtype=np.float64),
        velocity=np.zeros(3, dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )
    state.forces.append((np.array([10, 0, 0], dtype=np.float64), None))
    obj = PhysicalObject(shape="point", state=state, id="obj1")
    space = Space(dimensions=2)
    space.add(obj)
    fig = renderer.render(space)
    assert fig is not None
    renderer.close()


def test_matplotlib_2d_config() -> None:
    config = RenderConfig(resolution=(800, 600), background_color="black")
    renderer = Matplotlib2D(config)
    assert renderer.config.resolution == (800, 600)
    assert renderer.config.background_color == "black"


def test_matplotlib_2d_save_without_render() -> None:
    renderer = Matplotlib2D()
    try:
        renderer.save("/tmp/test.png")
        assert False
    except RuntimeError as e:
        assert "render()" in str(e)


def test_matplotlib_2d_close() -> None:
    renderer = Matplotlib2D()
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
    space = Space(dimensions=2)
    space.add(obj)
    renderer.render(space)
    renderer.close()
    assert renderer._fig is None
