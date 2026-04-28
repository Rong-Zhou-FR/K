# AGENTS-core.md — Core Abstractions Agent Instructions

## Summary

Core abstractions defining the fundamental interfaces for K: Space, PhysicalObject, Subsystem, State, and PhysicsPlugin.

## Purpose and Expected Behavior

- `Space`: Container for 2D/3D simulations, manages objects and domains
- `PhysicalObject`: Base class for all physics objects (rigid bodies, particles, etc.)
- `Subsystem`: Group of related objects
- `State`: Dataclass tracking all physical properties of an object
- `PhysicsPlugin`: Protocol for physics domain implementations

## Constraints and Invariants

- `Space` must track enabled domains and pass them to solver
- `PhysicalObject` must have a `State` instance always initialized
- `State` fields must be numpy arrays for vectorized computation
- Objects added to Space must have unique IDs
- Domain enable/disable must update both Space and Object states

## Core Classes API

```python
from numpy.typing import NDArray

@dataclass
class State:
    position: NDArray[np.float64]
    velocity: NDArray[np.float64]
    acceleration: NDArray[np.float64]
    orientation: NDArray[np.float64]
    angular_velocity: NDArray[np.float64]
    mass: float
    inertia: NDArray[np.float64]
    # ... (see 0-init-plan.md for full State model)

class PhysicalObject:
    id: str
    state: State
    shape: str  # "box", "sphere", "cylinder", etc.

    def apply(self, influence: Any) -> None: ...
    def enable_domain(self, domain: str) -> None: ...
    def disable_domain(self, domain: str) -> None: ...
```

## Input/Output Expectations

- Inputs: shape type, dimensions, mass, initial position/velocity
- Outputs: Object with initialized State ready for simulation

## Documentation Reference

- `docs/man/core/space.md`
- `docs/man/core/object.md`
- `docs/man/core/state.md`

## Domain-Specific Rules for Agents

- Add new shapes to `PhysicalObject.shape` union type
- Add new State fields only with default values for backward compatibility
- New core classes must implement `__repr__` for debugging
- Serialization format: JSON with numpy array encoding
