from __future__ import annotations

from k.core.object import PhysicalObject
from k.core.plugin import PhysicsPlugin
from k.core.space import Space
from k.physics.mechanics.dynamics import compute_net_wrench


class MechanicsPlugin:
    name = "mechanics"
    version = "0.1.0"

    def initialize(self, space: Space) -> None:
        space.enable_domain("mechanics")

    def compute_accelerations(
        self, objects: list[PhysicalObject], dt: float
    ) -> None:
        for obj in objects:
            if "mechanics" in obj.state.enabled_domains:
                compute_net_wrench(obj.state)

    def step(self, space: Space, dt: float) -> None:
        pass
