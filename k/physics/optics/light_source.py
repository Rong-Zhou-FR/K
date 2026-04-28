from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from k.core.state import Vector3T

SPEED_OF_LIGHT = 299_792_458.0


@dataclass
class LightSource:
    position: Vector3T
    intensity: float
    wavelength: float
    spectral_width: float = 0.0
    coherence_length: float = 0.0

    @property
    def frequency(self) -> float:
        return SPEED_OF_LIGHT / self.wavelength

    @property
    def angular_frequency(self) -> float:
        return 2 * np.pi * self.frequency

    def emit_ray(self, direction: Vector3T) -> "Ray":
        from k.physics.optics.ray import Ray

        norm = np.linalg.norm(direction)
        if norm == 0:
            raise ValueError("Direction cannot be zero vector")
        return Ray(
            origin=self.position.copy(),
            direction=direction / norm,
            wavelength=self.wavelength,
            normalized=True,
        )
