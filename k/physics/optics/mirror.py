from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from k.core.state import Vector3T
from k.physics.optics.optical_element import OpticalElement, PlaneSurface
from k.physics.optics.ray import Ray
from k.physics.optics.snell import reflect


@dataclass
class Mirror(OpticalElement):
    normal: Vector3T
    position: Vector3T
    curvature_type: str = "plane"

    def __post_init__(self) -> None:
        norm = np.linalg.norm(self.normal)
        if norm > 0:
            self.normal = self.normal / norm

    @property
    def surface(self) -> PlaneSurface:
        return PlaneSurface(position=self.position, normal=self.normal)

    def intersect(self, ray: Ray) -> tuple[float, bool]:
        t = self.surface.intersect_ray(ray)
        return (t if t is not None else float("inf"), t is not None and t > 0)

    def refract(self, ray: Ray) -> Ray | None:
        return None

    def reflect(self, ray: Ray) -> Ray:
        t, hit = self.intersect(ray)
        if not hit:
            raise ValueError("Ray does not intersect mirror")
        hit_point = ray.at(t)
        new_origin = hit_point + 1e-6 * self.normal
        return reflect(ray=ray, normal=self.normal)

    def trace(self, ray: Ray) -> list[Ray]:
        return [self.reflect(ray)]


@dataclass
class FlatMirror(Mirror):
    def __init__(self, normal: Vector3T, position: Vector3T) -> None:
        self.normal = normal
        self.position = position
        self.curvature_type = "plane"


@dataclass
class ConcaveMirror(Mirror):
    radius_of_curvature: float = 1.0
    aperture: float = 0.05

    def intersect(self, ray: Ray) -> tuple[float, bool]:
        oc = self.position
        ro = ray.origin - oc
        a = np.dot(ray.direction, ray.direction)
        b = 2.0 * np.dot(ro, ray.direction)
        c = np.dot(ro, ro) - self.radius_of_curvature**2
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return float("inf"), False
        sqrt_d = np.sqrt(discriminant)
        t1 = (-b - sqrt_d) / (2 * a)
        t2 = (-b + sqrt_d) / (2 * a)
        t = t1 if t1 > 0 else (t2 if t2 > 0 else float("inf"))
        return (t if t > 0 else float("inf")), t > 0
