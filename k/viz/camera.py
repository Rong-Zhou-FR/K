from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

Vector3T = NDArray[np.float64]


class CameraAngle:
    def __init__(
        self,
        position: Vector3T,
        focal_point: Vector3T | None = None,
        view_up: Vector3T | None = None,
    ) -> None:
        self.position = position
        self.focal_point = (
            focal_point
            if focal_point is not None
            else np.array([0, 0, 0], dtype=np.float64)
        )
        self.view_up = (
            view_up if view_up is not None else np.array([0, 0, 1], dtype=np.float64)
        )


class CameraPreset:
    @staticmethod
    def top() -> CameraAngle:
        return CameraAngle(position=np.array([0, 0, 10], dtype=np.float64))

    @staticmethod
    def front() -> CameraAngle:
        return CameraAngle(position=np.array([10, 0, 0], dtype=np.float64))

    @staticmethod
    def side() -> CameraAngle:
        return CameraAngle(position=np.array([0, 10, 0], dtype=np.float64))

    @staticmethod
    def isometric() -> CameraAngle:
        return CameraAngle(position=np.array([8, 8, 8], dtype=np.float64))
