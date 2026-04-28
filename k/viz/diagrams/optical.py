from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from k.core.space import Space

Vector3T = NDArray[np.float64]


class OpticalDiagram:
    def __init__(
        self,
        ray_color: str = "yellow",
        lens_color: str = "blue",
        mirror_color: str = "gray",
    ) -> None:
        self.ray_color = ray_color
        self.lens_color = lens_color
        self.mirror_color = mirror_color

    def draw_rays_2d(
        self,
        space: Space,
        ax: Any,
    ) -> None:
        for obj in space.objects.values():
            if hasattr(obj, "shape") and obj.shape == "ray":
                if hasattr(obj, "path") and obj.path:
                    path = np.array(obj.path)
                    ax.plot(
                        path[:, 0],
                        path[:, 1],
                        color=self.ray_color,
                        linewidth=2,
                        alpha=0.8,
                        label="ray" if not hasattr(ax, "_ray_label_drawn") else None,
                    )
                    ax._ray_label_drawn = True

    def draw_optical_elements_2d(
        self,
        space: Space,
        ax: Any,
    ) -> None:
        for obj in space.objects.values():
            if hasattr(obj, "shape"):
                pos = obj.state.position
                if "lens" in obj.shape:
                    self._draw_lens_2d(pos, ax)
                elif "mirror" in obj.shape:
                    self._draw_mirror_2d(pos, ax)

    def _draw_lens_2d(self, pos: Vector3T, ax: Any) -> None:
        ax.axvline(
            x=pos[0],
            color=self.lens_color,
            linewidth=3,
            alpha=0.6,
            label="lens" if not hasattr(ax, "_lens_label_drawn") else None,
        )
        ax._lens_label_drawn = True

    def _draw_mirror_2d(self, pos: Vector3T, ax: Any) -> None:
        ax.axvline(
            x=pos[0],
            color=self.mirror_color,
            linewidth=3,
            linestyle="--",
            alpha=0.6,
            label="mirror" if not hasattr(ax, "_mirror_label_drawn") else None,
        )
        ax._mirror_label_drawn = True

    def draw_rays_3d(
        self,
        space: Space,
        plotter: Any,
    ) -> None:
        import pyvista as pv

        for obj in space.objects.values():
            if hasattr(obj, "shape") and obj.shape == "ray":
                if hasattr(obj, "path") and obj.path:
                    path = np.array(obj.path)
                    poly = pv.lines_from_points(path)
                    plotter.add_mesh(
                        poly, color=self.ray_color, line_width=3, opacity=0.8
                    )

    def draw_optical_elements_3d(
        self,
        space: Space,
        plotter: Any,
    ) -> None:
        for obj in space.objects.values():
            if hasattr(obj, "shape"):
                pos = obj.state.position
                if "lens" in obj.shape:
                    self._draw_lens_3d(pos, plotter)
                elif "mirror" in obj.shape:
                    self._draw_mirror_3d(pos, plotter)

    def _draw_lens_3d(self, pos: Vector3T, plotter: Any) -> None:
        import pyvista as pv

        plane = pv.Plane(center=pos, direction=(1, 0, 0), i_size=2, j_size=2)
        plotter.add_mesh(plane, color=self.lens_color, opacity=0.5)

    def _draw_mirror_3d(self, pos: Vector3T, plotter: Any) -> None:
        import pyvista as pv

        plane = pv.Plane(center=pos, direction=(1, 0, 0), i_size=2, j_size=2)
        plotter.add_mesh(plane, color=self.mirror_color, opacity=0.7)
