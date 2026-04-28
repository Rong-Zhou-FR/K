from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from k.core.space import Space


@dataclass
class RenderConfig:
    resolution: tuple[int, int] = (1920, 1080)
    background_color: str = "white"
    show_axes: bool = True
    show_grid: bool = True
    color_by_domain: bool = True


class Renderer(ABC):
    @abstractmethod
    def render(self, space: Space) -> Any: ...

    @property
    @abstractmethod
    def dimensions(self) -> int: ...
