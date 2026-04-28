from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from k.core.object import PhysicalObject
from k.core.state import State


@dataclass
class CollisionSphere:
    radius: float


@dataclass
class CollisionBox:
    half_extents: np.ndarray


@dataclass
class CollisionCapsule:
    radius: float
    half_height: float


class RigidBody(PhysicalObject):
    def __init__(
        self,
        shape: str,
        state: State,
        collision_shape: CollisionSphere | CollisionBox | CollisionCapsule | None = None,
        id: str | None = None,
    ) -> None:
        super().__init__(shape, state, id)
        self.collision_shape = collision_shape
