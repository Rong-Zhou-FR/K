from __future__ import annotations

import numpy as np
from k.viz.pyvista_3d import PyVista3D
from k.viz.base import RenderConfig
from k.viz.camera import CameraPreset
from k.core.state import State
from k.core.object import PhysicalObject
from k.core.space import Space


def test_pyvista_3d_dimensions() -> None:
    renderer = PyVista3D()
    assert renderer.dimensions == 3


def test_pyvista_3d_render_empty_space() -> None:
    renderer = PyVista3D()
    space = Space(dimensions=3)
    plotter = renderer.render(space)
    assert plotter is not None
    plotter.close()


def test_pyvista_3d_render_with_object() -> None:
    renderer = PyVista3D()
    state = State(
        position=np.array([1, 2, 3], dtype=np.float64),
        velocity=np.zeros(3, dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )
    obj = PhysicalObject(shape="sphere", state=state, id="obj1")
    space = Space(dimensions=3)
    space.add(obj)
    plotter = renderer.render(space)
    assert plotter is not None
    plotter.close()


def test_pyvista_3d_with_camera_angle() -> None:
    renderer = PyVista3D()
    cam = CameraPreset.isometric()
    renderer.add_camera_angle(cam)
    assert len(renderer._camera_angles) == 1


def test_pyvista_3d_render_with_force() -> None:
    renderer = PyVista3D()
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
    state.wrenches.append((wrench, state.position.copy()))
    obj = PhysicalObject(shape="box", state=state, id="obj1")
    space = Space(dimensions=3)
    space.add(obj)
    plotter = renderer.render(space)
    assert plotter is not None
    plotter.close()


def test_pyvista_3d_config() -> None:
    config = RenderConfig(resolution=(800, 600), background_color="black")
    renderer = PyVista3D(config)
    assert renderer.config.resolution == (800, 600)


def test_pyvista_3d_save_without_render() -> None:
    renderer = PyVista3D()
    try:
        renderer.save_screenshot("/tmp/test.png")
        assert False
    except RuntimeError as e:
        assert "render()" in str(e)
