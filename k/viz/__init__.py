from __future__ import annotations

from k.viz.base import RenderConfig, Renderer
from k.viz.camera import CameraAngle, CameraPreset
from k.viz.colors import DOMAIN_COLORS, get_domain_color, get_object_color
from k.viz.diagrams import ForceDiagram, OpticalDiagram

__all__ = [
    "Renderer",
    "RenderConfig",
    "Matplotlib2D",
    "PyVista3D",
    "ForceDiagram",
    "OpticalDiagram",
    "Animation",
    "ExportManager",
    "CameraAngle",
    "CameraPreset",
    "DOMAIN_COLORS",
    "get_domain_color",
    "get_object_color",
    "create_renderer",
]


def create_renderer(renderer_type: str, config: RenderConfig | None = None) -> Renderer:
    if renderer_type == "matplotlib":
        from k.viz.matplotlib_2d import Matplotlib2D

        return Matplotlib2D(config)
    elif renderer_type == "pyvista":
        from k.viz.pyvista_3d import PyVista3D

        return PyVista3D(config)
    else:
        raise ValueError(f"Unknown renderer type: {renderer_type}")


from k.viz.animation import Animation
from k.viz.export import ExportManager
from k.viz.matplotlib_2d import Matplotlib2D
from k.viz.pyvista_3d import PyVista3D
