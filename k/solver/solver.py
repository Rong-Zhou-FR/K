from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from k.core.object import PhysicalObject
    from k.core.plugin import PhysicsPlugin
    from k.core.space import Space
    from k.solver.integrator import Integrator

from k.physics.mechanics.dynamics import compute_net_wrench


class Solver:
    def __init__(
        self,
        space: Space,
        integrator: Integrator,
        dt: float = 0.01,
    ) -> None:
        if dt <= 0:
            raise ValueError("dt must be positive")
        self.space = space
        self.integrator = integrator
        self.dt = dt
        self.time: float = 0.0
        self._plugins: list[PhysicsPlugin] = []

    def register_plugin(self, plugin: PhysicsPlugin) -> None:
        plugin.initialize(self.space)
        self._plugins.append(plugin)

    def step(self, n: int = 1) -> None:
        for _ in range(n):
            for plugin in self._plugins:
                plugin.compute_accelerations(
                    list(self.space.objects.values()), self.dt
                )
            for obj in self.space.objects.values():
                compute_net_wrench(obj.state)
                self.integrator.step(obj.state, self.dt)
            for plugin in self._plugins:
                plugin.step(self.space, self.dt)
            self.time += self.dt

    def run(self, duration: float) -> None:
        steps = int(duration / self.dt)
        self.step(steps)
