# AGENTS-calc.md — Calculation Utilities Agent Instructions

## Summary

Calculation utilities: kinematics, energy, fields, and math helpers for physics calculations.

## Purpose and Expected Behavior

Pure calculation functions independent of simulation:
- Kinematics (position, velocity, acceleration)
- Energy calculations (kinetic, potential, work)
- Field calculations (gravitational, electric, magnetic)
- Vector math helpers

## Constraints and Invariants

- All calculations pure (no side effects)
- Input validation on all public functions
- Vectorized numpy operations where possible
- Return numpy arrays, not lists

## Key Functions

```python
from numpy.typing import NDArray

def kinetic_energy(m: float, v: NDArray[np.float64]) -> float: ...
def potential_energy(m: float, g: float, h: float) -> float: ...
def work(force: NDArray[np.float64], displacement: NDArray[np.float64]) -> float: ...
def gravitational_field(M: float, position: NDArray[np.float64]) -> NDArray[np.float64]: ...
def relative_velocity(v1: NDArray[np.float64], v2: NDArray[np.float64]) -> NDArray[np.float64]: ...
def angle_between(v1: NDArray[np.float64], v2: NDArray[np.float64]) -> float: ...
```

## Documentation Reference

- `docs/man/calc/index.md`
- `docs/man/calc/energy.md`

## Domain-Specific Rules for Agents

- Pure functions: no state modification
- Type hints on all inputs/outputs
- Vectorized operations preferred
- Document units for each calculation