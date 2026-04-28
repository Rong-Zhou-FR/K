from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from k.core.object import PhysicalObject
from k.core.space import Space
from k.viz.base import RenderConfig, Renderer
from k.viz.colors import get_object_color

Vector3T = NDArray[np.float64]


class Matplotlib2D(Renderer):
    def __init__(self, config: RenderConfig | None = None) -> None:
        self.config = config or RenderConfig()
        self._fig = None
        self._ax = None

    @property
    def dimensions(self) -> int:
        return 2

    def render(self, space: Space) -> Any:
        import matplotlib.pyplot as plt

        self._fig, self._ax = plt.subplots(figsize=self._compute_figure_size())
        self._ax.set_facecolor(self.config.background_color)

        if self.config.show_grid:
            self._ax.grid(True, alpha=0.3)

        if self.config.show_axes:
            self._ax.axhline(y=0, color="k", linestyle="-", alpha=0.3)
            self._ax.axvline(x=0, color="k", linestyle="-", alpha=0.3)

        for obj in space.objects.values():
            self._render_object(obj)

        self._ax.set_aspect("equal")
        self._ax.set_xlabel("X")
        self._ax.set_ylabel("Y")
        return self._fig

    def _render_object(self, obj: PhysicalObject) -> None:
        import matplotlib.pyplot as plt

        pos = obj.state.position
        color = get_object_color(obj) if self.config.color_by_domain else "blue"

        if obj.shape in ("point", "particle"):
            self._ax.scatter(pos[0], pos[1], c=color, s=100, label=obj.id)
        elif obj.shape == "sphere":
            circle = plt.Circle((pos[0], pos[1]), 0.5, color=color, alpha=0.6)
            self._ax.add_patch(circle)
        elif obj.shape == "box":
            rect = plt.Rectangle(
                (pos[0] - 0.5, pos[1] - 0.5), 1, 1, color=color, alpha=0.6
            )
            self._ax.add_patch(rect)
        else:
            self._ax.scatter(pos[0], pos[1], c=color, s=50, marker="x")

        self._render_forces(obj)

    def _render_forces(self, obj: PhysicalObject) -> None:
        pos = obj.state.position
        for force, point in obj.state.forces:
            origin = point if point is not None else pos
            self._ax.arrow(
                origin[0],
                origin[1],
                force[0] * 0.1,
                force[1] * 0.1,
                head_width=0.1,
                head_length=0.1,
                fc="red",
                ec="red",
                alpha=0.7,
            )

    def _compute_figure_size(self) -> tuple[float, float]:
        dpi = 100
        w, h = self.config.resolution
        return (w / dpi, h / dpi)

    def save(self, path: str, fmt: str = "png") -> None:
        if self._fig is None:
            raise RuntimeError("Must call render() before save()")
        self._fig.savefig(path, format=fmt, dpi=100, bbox_inches="tight")

    def show(self) -> None:
        import matplotlib.pyplot as plt

        if self._fig is None:
            raise RuntimeError("Must call render() before show()")
        plt.show()

    def close(self) -> None:
        import matplotlib.pyplot as plt

        if self._fig is not None:
            plt.close(self._fig)
            self._fig = None
            self._ax = None
