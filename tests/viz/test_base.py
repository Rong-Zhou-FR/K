from __future__ import annotations

import pytest
from k.viz.base import RenderConfig, Renderer
from k.core.space import Space


class ConcreteRenderer(Renderer):
    def render(self, space: Space) -> None:
        return None

    @property
    def dimensions(self) -> int:
        return 2


def test_render_config_defaults() -> None:
    config = RenderConfig()
    assert config.resolution == (1920, 1080)
    assert config.background_color == "white"
    assert config.show_axes is True
    assert config.show_grid is True
    assert config.color_by_domain is True


def test_render_config_custom() -> None:
    config = RenderConfig(
        resolution=(800, 600), background_color="black", show_axes=False
    )
    assert config.resolution == (800, 600)
    assert config.background_color == "black"
    assert config.show_axes is False


def test_renderer_is_abstract() -> None:
    with pytest.raises(TypeError):
        Renderer()


def test_concrete_renderer() -> None:
    renderer = ConcreteRenderer()
    assert renderer.dimensions == 2
    assert renderer.render(None) is None
