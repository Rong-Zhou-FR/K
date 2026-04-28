from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from k.core.state import State, Vector3T, QuaternionT


class Integrator(ABC):
    @abstractmethod
    def step(self, state: State, dt: float) -> None:
        pass


class EulerIntegrator(Integrator):
    def step(self, state: State, dt: float) -> None:
        force = state.net_wrench[:3]
        torque = state.net_wrench[3:]
        state.acceleration = force / state.mass
        state.angular_acceleration = np.linalg.solve(state.inertia, torque)
        state.velocity += state.acceleration * dt
        state.angular_velocity += state.angular_acceleration * dt
        state.position += state.velocity * dt
        state.orientation = self._update_orientation(
            state.orientation, state.angular_velocity, dt
        )
        state.wrenches.clear()
        state.net_wrench = np.zeros(6, dtype=np.float64)

    def _update_orientation(
        self, q: QuaternionT, omega: Vector3T, dt: float
    ) -> QuaternionT:
        wx, wy, wz = omega
        half_dt = 0.5 * dt
        dq = np.array([0.0, wx, wy, wz]) * half_dt
        return self._quaternion_multiply(q, dq)

    def _quaternion_multiply(self, q1: QuaternionT, q2: QuaternionT) -> QuaternionT:
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        return np.array(
            [
                w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
                w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
            ],
            dtype=np.float64,
        )


class RK4Integrator(Integrator):
    def step(self, state: State, dt: float) -> None:
        force = state.net_wrench[:3]
        torque = state.net_wrench[3:]
        acc = force / state.mass
        ang_acc = np.linalg.solve(state.inertia, torque)

        v0 = state.velocity.copy()
        x0 = state.position.copy()

        k1_x = v0
        k1_v = acc

        k2_x = v0 + 0.5 * dt * k1_v
        k2_v = acc

        k3_x = v0 + 0.5 * dt * k2_v
        k3_v = acc

        k4_x = v0 + dt * k3_v
        k4_v = acc

        state.position = x0 + (dt / 6.0) * (k1_x + 2 * k2_x + 2 * k3_x + k4_x)
        state.velocity = v0 + (dt / 6.0) * (k1_v + 2 * k2_v + 2 * k3_v + k4_v)

        state.acceleration = acc
        state.angular_acceleration = ang_acc
        state.wrenches.clear()
        state.net_wrench = np.zeros(6, dtype=np.float64)


class VerletIntegrator(Integrator):
    def __init__(self) -> None:
        self._prev_acceleration: Vector3T | None = None

    def step(self, state: State, dt: float) -> None:
        force = state.net_wrench[:3]
        torque = state.net_wrench[3:]
        new_acc = force / state.mass

        if self._prev_acceleration is not None:
            state.position += (
                state.velocity * dt
                + 0.5 * (self._prev_acceleration + new_acc) * dt**2
            )
            state.velocity += 0.5 * (self._prev_acceleration + new_acc) * dt
        else:
            state.position += state.velocity * dt + 0.5 * new_acc * dt**2
            state.velocity += new_acc * dt

        state.acceleration = new_acc
        state.angular_acceleration = np.linalg.solve(state.inertia, torque)
        state.angular_velocity += state.angular_acceleration * dt
        self._prev_acceleration = new_acc
        state.wrenches.clear()
        state.net_wrench = np.zeros(6, dtype=np.float64)
