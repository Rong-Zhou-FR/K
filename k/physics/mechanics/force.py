from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass
class Force:
    force: NDArray[np.float64]
    point: NDArray[np.float64]

    def to_wrench(self) -> NDArray[np.float64]:
        wrench: NDArray[np.float64] = np.zeros(6, dtype=np.float64)
        wrench[:3] = self.force
        return wrench


@dataclass
class Torque:
    torque: NDArray[np.float64]

    def to_wrench(self) -> NDArray[np.float64]:
        wrench: NDArray[np.float64] = np.zeros(6, dtype=np.float64)
        wrench[3:] = self.torque
        return wrench
