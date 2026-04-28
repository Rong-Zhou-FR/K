from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from k.core.state import Vector3T
from k.physics.optics.ray import Ray


class OpticalElement(ABC):
    @abstractmethod
    def intersect(self, ray: Ray) -> tuple[float, bool]:
        raise NotImplementedError

    @abstractmethod
    def refract(self, ray: Ray) -> Ray | None:
        raise NotImplementedError

    @abstractmethod
    def reflect(self, ray: Ray) -> Ray:
        raise NotImplementedError

    @abstractmethod
    def trace(self, ray: Ray) -> list[Ray]:
        raise NotImplementedError


@dataclass
class PlaneSurface:
    position: Vector3T
    normal: Vector3T

    def __post_init__(self) -> None:
        norm = np.linalg.norm(self.normal)
        if norm > 0:
            self.normal = self.normal / norm

    def distance_to(self, point: Vector3T) -> float:
        return np.dot(point - self.position, self.normal)

    def intersect_ray(self, ray: Ray) -> float | None:
        denom = np.dot(ray.direction, self.normal)
        if abs(denom) < 1e-10:
            return None
        t = np.dot(self.position - ray.origin, self.normal) / denom
        return t if t > 0 else None
