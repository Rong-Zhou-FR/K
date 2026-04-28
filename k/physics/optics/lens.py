from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from k.core.state import Vector3T
from k.physics.optics.optical_element import OpticalElement, PlaneSurface
from k.physics.optics.ray import Ray
from k.physics.optics.snell import refract as snell_refract, reflect as snell_reflect


class CurvatureType(Enum):
    CONVEX = "convex"
    CONCAVE = "concave"
    PLANE = "plane"


@dataclass
class Lens(OpticalElement):
    focal_length: float
    center: Vector3T
    normal: Vector3T
    curvature_type: str = "convex"
    radius_of_curvature: float = 0.0
    thickness: float = 0.0
    material_n: float = 1.5

    def __post_init__(self) -> None:
        norm = np.linalg.norm(self.normal)
        if norm > 0:
            self.normal = self.normal / norm

    @property
    def front_surface(self) -> PlaneSurface:
        offset = self.thickness / 2 * self.normal
        return PlaneSurface(position=self.center + offset, normal=self.normal)

    @property
    def back_surface(self) -> PlaneSurface:
        offset = self.thickness / 2 * self.normal
        return PlaneSurface(position=self.center - offset, normal=-self.normal)

    def intersect(self, ray: Ray) -> tuple[float, bool]:
        t_front = self.front_surface.intersect_ray(ray)
        if t_front is not None and t_front > 0:
            return t_front, True
        return float("inf"), False

    def refract(self, ray: Ray) -> Ray | None:
        t = self.intersect(ray)[0]
        if t == float("inf"):
            return None
        return snell_refract(
            ray=ray,
            normal=self.front_surface.normal,
            n1=1.0,
            n2=self.material_n,
        )

    def reflect(self, ray: Ray) -> Ray:
        t = self.intersect(ray)[0]
        if t == float("inf"):
            raise ValueError("Ray does not intersect lens")
        return snell_reflect(ray=ray, normal=self.front_surface.normal)

    def trace(self, ray: Ray) -> list[Ray]:
        refracted = self.refract(ray)
        return [refracted] if refracted else []


@dataclass
class ThinLens(OpticalElement):
    focal_length: float
    center: Vector3T
    normal: Vector3T
    material_n: float = 1.5

    def __post_init__(self) -> None:
        norm = np.linalg.norm(self.normal)
        if norm > 0:
            self.normal = self.normal / norm

    def intersect(self, ray: Ray) -> tuple[float, bool]:
        denom = np.dot(ray.direction, self.normal)
        if abs(denom) < 1e-10:
            return float("inf"), False
        t = np.dot(self.center - ray.origin, self.normal) / denom
        return (t if t > 0 else float("inf")), t > 0

    def refract(self, ray: Ray) -> Ray | None:
        t, hit = self.intersect(ray)
        if not hit:
            return None
        return snell_refract(
            ray=ray,
            normal=self.normal,
            n1=1.0,
            n2=self.material_n,
        )

    def reflect(self, ray: Ray) -> Ray:
        return snell_reflect(ray=ray, normal=self.normal)

    def trace(self, ray: Ray) -> list[Ray]:
        t, hit = self.intersect(ray)
        if not hit:
            return []
        refracted = self.refract(ray)
        if refracted is None:
            return [self.reflect(ray)]
        return [refracted, self.reflect(ray)]
