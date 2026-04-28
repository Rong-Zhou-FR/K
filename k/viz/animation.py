from __future__ import annotations

from typing import Any

from k.core.space import Space
from k.viz.base import RenderConfig


class Animation:
    def __init__(
        self,
        frames: int = 100,
        fps: int = 30,
        config: RenderConfig | None = None,
    ) -> None:
        self.frames = frames
        self.fps = fps
        self.config = config or RenderConfig()

    def create_from_solver(
        self,
        space: Space,
        solver: Any,
        duration: float,
        output_path: str,
        renderer_type: str = "matplotlib",
    ) -> None:
        dt = duration / self.frames
        rendered_frames = []

        for i in range(self.frames):
            if renderer_type == "matplotlib":
                from k.viz.matplotlib_2d import Matplotlib2D

                renderer = Matplotlib2D(self.config)
                fig = renderer.render(space)
                rendered_frames.append(fig)
            elif renderer_type == "pyvista":
                from k.viz.pyvista_3d import PyVista3D

                renderer = PyVista3D(self.config)
                plotter = renderer.render(space)
                temp_path = f"/tmp/frame_{i:04d}.png"
                plotter.screenshot(temp_path)
                rendered_frames.append(temp_path)
            if solver:
                solver.step(space, dt)

        if output_path.endswith(".gif"):
            from k.viz.export import ExportManager

            ExportManager(self.config).export_frames_to_gif(
                rendered_frames, output_path, self.fps
            )
        elif output_path.endswith(".mp4"):
            from k.viz.export import ExportManager

            ExportManager(self.config).export_frames_to_mp4(
                rendered_frames, output_path, self.fps
            )

    def _create_manim_animation(self, frames: list[Any]) -> Any:
        try:
            import manim
        except ImportError as e:
            raise RuntimeError("manim is required for manim animations") from e
        return manim.Scene()
