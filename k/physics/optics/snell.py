from __future__ import annotations

import numpy as np

from k.core.state import Vector3T
from k.physics.optics.ray import Ray


def refract(
    ray: Ray,
    normal: Vector3T,
    n1: float = 1.0,
    n2: float = 1.5,
) -> Ray | None:
    n = n1 / n2
    cos_i = -np.dot(ray.direction, normal)
    sin_t2 = n**2 * (1.0 - cos_i**2)
    if sin_t2 > 1.0:
        return None
    cos_t = np.sqrt(1.0 - sin_t2)
    refracted_dir = n * ray.direction + (n * cos_i - cos_t) * normal
    return Ray(
        origin=ray.at(0.0),
        direction=refracted_dir,
        wavelength=ray.wavelength,
        normalized=True,
        phase=ray.phase,
    )


def reflect(ray: Ray, normal: Vector3T) -> Ray:
    reflected_dir = ray.direction - 2 * np.dot(ray.direction, normal) * normal
    return Ray(
        origin=ray.at(0.0),
        direction=reflected_dir,
        wavelength=ray.wavelength,
        normalized=True,
        phase=ray.phase,
    )


def snell_angle(theta_i: float, n1: float, n2: float) -> float | None:
    sin_t = (n1 / n2) * np.sin(theta_i)
    if abs(sin_t) > 1.0:
        return None
    return np.arcsin(sin_t)


def critical_angle(n1: float, n2: float) -> float | None:
    if n1 <= n2:
        return None
    return np.arcsin(n2 / n1)


def is_total_internal_reflection(theta_i: float, n1: float, n2: float) -> bool:
    if n1 <= n2:
        return False
    return np.sin(theta_i) >= n2 / n1
