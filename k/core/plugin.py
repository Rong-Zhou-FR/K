from __future__ import annotations

from typing import Protocol

from k.core.space import Space


class PhysicsPlugin(Protocol):
    name: str
    version: str

    def initialize(self, space: Space) -> None: ...

    def compute_accelerations(
        self, objects: list["PhysicalObject"], dt: float
    ) -> None: ...

    def step(self, space: Space, dt: float) -> None: ...
