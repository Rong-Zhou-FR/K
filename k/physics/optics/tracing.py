from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from k.core.state import Vector3T
from k.physics.optics.lens import Lens, ThinLens
from k.physics.optics.light_source import LightSource
from k.physics.optics.mirror import Mirror
from k.physics.optics.ray import Ray
from k.physics.optics.system import OpticalSystem


@dataclass
class RayTracer:
    system: OpticalSystem

    def trace_ray(self, ray: Ray) -> list[Ray]:
        return self.system.trace(ray)

    def trace_from_source(
        self,
        source: LightSource,
        direction: Vector3T,
    ) -> list[Ray]:
        ray = source.emit_ray(direction)
        return self.system.trace(ray)

    def trace_fan(
        self,
        source: LightSource,
        num_rays: int,
        aperture_angle: float = 0.1,
    ) -> list[list[Ray]]:
        rays = []
        base_dir = np.array([0.0, 0.0, 1.0])
        for i in range(num_rays):
            theta = (i / (num_rays - 1) - 0.5) * aperture_angle if num_rays > 1 else 0.0
            direction = base_dir + np.array([theta, theta, 0.0])
            direction = direction / np.linalg.norm(direction)
            ray = source.emit_ray(direction)
            rays.append(self.system.trace(ray))
        return rays

    def find_caustic(self, source: LightSource, num_rays: int = 50) -> list[Vector3T]:
        traced = self.trace_fan(source, num_rays)
        caustic_points = []
        for rays in traced:
            if rays:
                last_ray = rays[-1]
                t = 10.0
                caustic_points.append(last_ray.at(t))
        return caustic_points


def trace_through_optical_system(
    system: OpticalSystem,
    sources: list[LightSource],
    num_rays_per_source: int = 10,
) -> dict[str, list[list[Ray]]]:
    results = {}
    tracer = RayTracer(system)
    for i, source in enumerate(sources):
        key = f"source_{i}"
        results[key] = tracer.trace_fan(source, num_rays_per_source)
    return results
