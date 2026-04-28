from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray

from k.core.object import PhysicalObject
from k.core.space import Space
from k.viz.base import RenderConfig, Renderer
from k.viz.camera import CameraAngle
from k.viz.colors import get_object_color

Vector3T = NDArray[np.float64]


class PyVista3D(Renderer):
    def __init__(self, config: RenderConfig | None = None) -> None:
        self.config = config or RenderConfig()
        self._plotter = None
        self._camera_angles: list[CameraAngle] = []

    @property
    def dimensions(self) -> int:
        return 3

    def render(self, space: Space) -> Any:
        import pyvista as pv

        self._plotter = pv.Plotter(
            window_size=list(self.config.resolution),
            off_screen=True,
        )
        self._plotter.set_background(self.config.background_color)

        if self.config.show_axes:
            self._plotter.add_axes()

        if self.config.show_grid:
            self._plotter.add_box_axes()

        for obj in space.objects.values():
            self._render_object(obj)

        self._apply_camera_angles()
        return self._plotter

    def _render_object(self, obj: PhysicalObject) -> None:
        import pyvista as pv

        pos = obj.state.position
        color = get_object_color(obj) if self.config.color_by_domain else "blue"

        if obj.shape in ("point", "particle"):
            point = pv.PolyData(pos)
            self._plotter.add_mesh(
                point, color=color, point_size=10, render_points_as_spheres=True
            )
        elif obj.shape == "sphere":
            sphere = pv.Sphere(radius=0.5, center=pos)
            self._plotter.add_mesh(sphere, color=color, opacity=0.6)
        elif obj.shape == "box":
            box = pv.Box(
                bounds=(
                    pos[0] - 0.5,
                    pos[0] + 0.5,
                    pos[1] - 0.5,
                    pos[1] + 0.5,
                    pos[2] - 0.5,
                    pos[2] + 0.5,
                )
            )
            self._plotter.add_mesh(box, color=color, opacity=0.6)
        else:
            point = pv.PolyData(pos)
            self._plotter.add_mesh(point, color=color, point_size=5)

        self._render_forces(obj)

    def _render_forces(self, obj: PhysicalObject) -> None:
        import pyvista as pv

        pos = obj.state.position
        for force, point in obj.state.forces:
            origin = point if point is not None else pos
            scaled_force = force * 0.1
            arrow = pv.Arrow(
                start=origin,
                direction=scaled_force,
                scale=1.0,
            )
            self._plotter.add_mesh(arrow, color="red", opacity=0.7)

    def add_camera_angle(self, angle: CameraAngle) -> None:
        self._camera_angles.append(angle)

    def _apply_camera_angles(self) -> None:
        if not self._camera_angles or self._plotter is None:
            return
        first = self._camera_angles[0]
        self._plotter.camera_position = (
            first.position,
            first.focal_point,
            first.view_up,
        )

    def save_screenshot(self, path: str) -> None:
        if self._plotter is None:
            raise RuntimeError("Must call render() before save_screenshot()")
        self._plotter.screenshot(path)

    def save_rotation_animation(self, path: str, frames: int = 60) -> None:
        if self._plotter is None:
            raise RuntimeError("Must call render() before save_rotation_animation()")
        self._plotter.open_gif(path)
        for _ in range(frames):
            self._plotter.write_frame()
            self._plotter.camera.azimuth += 360 / frames
        self._plotter.close()
