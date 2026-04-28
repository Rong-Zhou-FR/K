# AGENTS-optics.md — Optics Agent Instructions

## Summary

Optics module: ray tracing, lenses, mirrors, light sources, and optical systems.

## Purpose and Expected Behavior

Light/optics calculations:
- Ray tracing (geometric optics)
- Snell's law for refraction
- thin lens and mirror equations
- Light intensity and propagation

## Constraints and Invariants

- All optics calculations use SI units
- Wavelength: meters (m), typically 380-750 nm for visible
- Index of refraction: dimensionless (n ≥ 1)
- Speed of light in vacuum: c = 299,792,458 m/s

## Key Classes

```python
from numpy import ndarray
from numpy.typing import NDArray
from typing import Literal

Vector3T = NDArray[np.float64, Literal[3]]

class Ray:
    origin: Vector3T
    direction: Vector3T
    wavelength: float
    normalized: bool
    phase: float = 0.0

class LightSource:
    position: Vector3T
    intensity: float
    wavelength: float
    spectral_width: float = 0.0
    coherence_length: float = 0.0

class Lens:
    focal_length: float
    center: Vector3T
    normal: Vector3T
    curvature_type: str  # "convex" or "concave"
    radius_of_curvature: float
    thickness: float
    material_n: float  # index of refraction

class Mirror:
    normal: Vector3T
    position: Vector3T
```

## Documentation Reference

- `docs/man/physics/optics/index.md`
- `docs/man/physics/optics/ray_tracing.md`

## Domain-Specific Rules for Agents

- Support geometric optics only (wave optics optional)
- Implement Snell's law for refraction, Descarte's law for reflection, and thin les law for lens.
- Handle total internal reflection
- Allow multiple surfaces (optical systems)
