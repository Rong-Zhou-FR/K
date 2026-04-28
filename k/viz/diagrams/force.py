from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from k.core.object import PhysicalObject
from k.core.state import Vector3T

Vector3T = NDArray[np.float64]


class ForceDiagram:
    def __init__(
        self,
        scale: float = 0.1,
        color: str = "red",
    ) -> None:
        self.scale = scale
        self.color = color

    def draw_on_object_2d(
        self,
        obj: PhysicalObject,
        ax: Any,
    ) -> None:
        position = obj.state.position
        for wrench, point in obj.state.wrenches:
            force = wrench[:3]
            origin = point if point is not None else position
            ax.arrow(
                origin[0],
                origin[1],
                force[0] * self.scale,
                force[1] * self.scale,
                head_width=0.1,
                head_length=0.1,
                fc=self.color,
                ec=self.color,
                alpha=0.7,
                label="force" if not hasattr(ax, "_force_label_drawn") else None,
            )
            ax._force_label_drawn = True

    def draw_on_object_3d(
        self,
        obj: PhysicalObject,
        plotter: Any,
    ) -> None:
        import pyvista as pv

        position = obj.state.position
        for wrench, point in obj.state.wrenches:
            force = wrench[:3]
            origin = point if point is not None else position
            scaled_force = force * self.scale
            arrow = pv.Arrow(
                start=origin,
                direction=scaled_force,
                scale=1.0,
            )
            plotter.add_mesh(arrow, color=self.color, opacity=0.7)
