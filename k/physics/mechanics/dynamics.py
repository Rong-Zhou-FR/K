from __future__ import annotations

import numpy as np

from k.core.object import PhysicalObject
from k.core.state import State, Wrench6T, Vector3T
from k.physics.mechanics.force import Force, Torque


def compute_net_wrench(state: State) -> Wrench6T:
    net: Wrench6T = np.zeros(6, dtype=np.float64)
    for wrench, point in state.wrenches:
        r = point - state.position
        moment = np.cross(r, wrench[:3])
        net[:3] += wrench[:3]
        net[3:] += wrench[3:] + moment
    state.net_wrench = net
    return net


def apply_force(obj: PhysicalObject, force: Force) -> None:
    obj.apply(force)


def apply_torque(obj: PhysicalObject, torque: Torque) -> None:
    obj.apply(torque)


def net_force(wrenches: list[tuple[Wrench6T, Vector3T]]) -> Vector3T:
    net: Vector3T = np.zeros(3, dtype=np.float64)
    for wrench, _ in wrenches:
        net += wrench[:3]
    return net


def net_torque(wrenches: list[tuple[Wrench6T, Vector3T]], state: State) -> Vector3T:
    net: Vector3T = np.zeros(3, dtype=np.float64)
    for wrench, point in wrenches:
        r = point - state.position
        moment = np.cross(r, wrench[:3])
        net += wrench[3:] + moment
    return net
