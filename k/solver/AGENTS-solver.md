# AGENTS-solver.md — Simulation Engine Agent Instructions

## Summary

Simulation engine: time integration, solver orchestration, and step scheduling.

## Purpose and Expected Behavior

Manages simulation time evolution:
- Time integration (Euler, RK4, etc.)
- Orchestrates physics plugins each step
- Handles time step scheduling (fixed vs adaptive)
- Main simulation loop

## Constraints and Invariants

- All time units: seconds (s)
- Time step: dt must be positive
- Solver must preserve energy (configurable tolerance)
- Parallel object updates when possible

## Key Classes

```python
class Integrator(ABC):
    @abstractmethod
    def step(self, state: State, dt: float) -> State: ...

class EulerIntegrator(Integrator): ...
class RK4Integrator(Integrator): ...

class Solver:
    space: Space
    integrator: Integrator
    dt: float

    def step(self, n: int = 1) -> None: ...
    def run(self, duration: float) -> None: ...
```

## Documentation Reference

- `docs/man/solver/index.md`
- `docs/man/solver/integrator.md`

## Integration Points

- Uses `core/Space` for object list
- Uses `physics/*` plugins for physics updates
- Outputs to `viz/` for visualization

## Domain-Specific Rules for Agents

- RK4 as default integrator (balance speed/accuracy)
- Support both fixed and adaptive time steps
- Track simulation time and frame count
- Allow pause/resume