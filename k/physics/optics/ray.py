from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from k.core.state import Vector3T

SPEED_OF_LIGHT = 299_792_458.0


@dataclass
class Ray:
    origin: Vector3T
    direction: Vector3T
    wavelength: float
    normalized: bool = False
    phase: float = 0.0

    def __post_init__(self) -> None:
        if not self.normalized:
            norm = np.linalg.norm(self.direction)
            if norm > 0:
                self.direction = self.direction / norm
                self.normalized = True

    @property
    def frequency(self) -> float:
        return SPEED_OF_LIGHT / self.wavelength

    @property
    def angular_frequency(self) -> float:
        return 2 * np.pi * self.frequency

    @property
    def wave_number(self) -> float:
        return 2 * np.pi / self.wavelength

    @property
    def intensity(self) -> float:
        return 1.0

    def at(self, distance: float) -> Vector3T:
        return self.origin + distance * self.direction
