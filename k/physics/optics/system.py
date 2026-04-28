from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from k.core.state import Vector3T
from k.physics.optics.optical_element import OpticalElement
from k.physics.optics.ray import Ray


@dataclass
class OpticalSystem:
    elements: list[OpticalElement] = field(default_factory=list)

    def add(self, element: OpticalElement) -> None:
        self.elements.append(element)

    def trace(self, ray: Ray) -> list[Ray]:
        current_ray = ray
        traced_rays: list[Ray] = []
        max_bounces = 100
        for _ in range(max_bounces):
            closest_t = float("inf")
            closest_element: OpticalElement | None = None
            for element in self.elements:
                t, hit = element.intersect(current_ray)
                if hit and t < closest_t:
                    closest_t = t
                    closest_element = element
            if closest_element is None:
                break
            hit_point = current_ray.at(closest_t)
            traced = closest_element.trace(current_ray)
            if not traced:
                break
            traced_rays.extend(traced)
            current_ray = traced[0]
            if closest_element not in self.elements[-1:]:
                current_ray.origin = hit_point + 1e-6 * current_ray.direction
        return traced_rays

    def trace_to_focal_point(self, ray: Ray) -> Vector3T | None:
        from k.core.state import Vector3T

        traced = self.trace(ray)
        if traced:
            last_ray = traced[-1]
            if last_ray is not None:
                origin = last_ray.origin
                direction = last_ray.direction
                plane_normal = (
                    direction
                    if np.abs(np.dot(direction, np.array([0, 0, 1]))) < 0.9
                    else np.array([0, 0, 1])
                )
                plane_point = np.array([0.0, 0.0, 0.0])
                denom = np.dot(direction, plane_normal)
                if abs(denom) > 1e-10:
                    t = np.dot(plane_point - origin, plane_normal) / denom
                    if t > 0:
                        return origin + t * direction
        return None


@dataclass
class CompoundLens(OpticalSystem):
    def __init__(self, focal_length: float) -> None:
        super().__init__()
        self._focal_length = focal_length

    @property
    def effective_focal_length(self) -> float:
        f1 = getattr(self.elements[0], "focal_length", None) if self.elements else None
        f2 = (
            getattr(self.elements[1], "focal_length", None)
            if len(self.elements) > 1
            else None
        )
        if f1 is not None and f2 is not None:
            d = 0.0
            return 1.0 / (1.0 / f1 + 1.0 / f2 - d / (f1 * f2))
        return self._focal_length
