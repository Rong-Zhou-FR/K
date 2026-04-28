# AGENTS-mechanics.md — Classical Mechanics Agent Instructions

## Summary

Classical mechanics module: rigid body dynamics, forces, torques, collisions, and particle systems.

## Purpose and Expected Behavior

Physics calculations based on Newton's laws:
- Force application and net force calculation
- Torque and angular momentum
- Rigid body kinematics/dynamics
- Collision detection and resolution
- Particle motion

## Constraints and Invariants

- All mechanics calculations use SI units
- Force units: Newtons (N)
- Torque units: Newton-meters (N·m)
- Mass units: kilograms (kg)
- Position units: meters (m)

## Key Classes

```python
from numpy.typing import NDArray

class Force:
    vector: NDArray[np.float64]  # 3D force vector
    point: NDArray[np.float64]  # application point

class Torque:
    vector: NDArray[np.float64]  # 3D torque vector

class RigidBody(PhysicalObject):
    # Inherits from PhysicalObject
    # Adds collision shapes, constraints, joints

class Particle(PhysicalObject):
    # Point mass with no rotational inertia
    pass

def apply_force(obj: PhysicalObject, force: Force) -> None: ...
def net_force(forces: list[tuple[NDArray[np.float64], NDArray[np.float64]]]) -> NDArray[np.float64]: ...
def apply_torque(obj: RigidBody, torque: Torque) -> None: ...
def collision_detection(obj_a: PhysicalObject, obj_b: PhysicalObject) -> bool: ...
```

## Documentation Reference

- `docs/man/physics/mechanics/index.md`
- `docs/man/physics/mechanics/force.md`
- `docs/man/physics/mechanics/collision.md`

## Integration Points

- Connected to `solver/` for time integration
- Connected to `viz/` for force diagrams
- Optional backend: `pymunk` for 2D, `pydy`/`rbdl` for 3D

## Domain-Specific Rules for Agents

- Build mechanics from scratch for transparency (no external libs unless requested)
- Implement conservation laws explicitly
- Support both 2D and 3D calculations
- Collision resolution: elastic and inelastic options