from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

Vector3T = NDArray[np.float64]
QuaternionT = NDArray[np.float64]
InertiaTensorT = NDArray[np.float64]
Wrench6T = NDArray[np.float64]


@dataclass
class State:
    position: Vector3T
    velocity: Vector3T
    acceleration: Vector3T
    orientation: QuaternionT
    angular_velocity: Vector3T
    mass: float
    inertia: InertiaTensorT
    angular_acceleration: Vector3T = field(
        default_factory=lambda: np.zeros(3, dtype=np.float64)
    )

    temperature: float = 298.15
    heat_capacity: float = 1.0
    thermal_conductivity: float = 0.0

    charge: float = 0.0
    current: Vector3T = field(default_factory=lambda: np.zeros(3, dtype=np.float64))
    magnetic_moment: Vector3T = field(default_factory=lambda: np.zeros(3, dtype=np.float64))

    wrenches: list[tuple[Wrench6T, Vector3T]] = field(default_factory=list)
    net_wrench: Wrench6T = field(default_factory=lambda: np.zeros(6, dtype=np.float64))
    heat_flows: list[tuple[float, Vector3T]] = field(default_factory=list)

    enabled_domains: set[str] = field(default_factory=lambda: {"mechanics"})
