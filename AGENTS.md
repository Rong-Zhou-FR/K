# AGENTS.md — K Project Rules for AI Agents

This is the canonical, repo-wide instruction file for AI agents working on **K**.

## Hierarchical Context Model

Agents **must** follow this rule:

> When working inside a directory, load the nearest `AGENTS.md` file and merge it with parent `AGENTS.md` files up to root.  
> Local rules override global rules.

Context resolution order (highest priority first):
1. `AGENTS-[module].md` in module directories — module-specific context
2. `AGENTS.md` in current working directory (if present)
3. Root `AGENTS.md` — global project rules

---

## Project Overview

**K** is a Python library for 3D classical physics simulation, calculation, and visualization.
- Covers all major branches of classical physics (mechanics, thermodynamics, electromagnetism, optics, fluid dynamics)
- Target audience: grade-school to bachelor's degree level education
- 100% FOSS: zero proprietary dependencies
- Modular: user enables only needed physics domains
- Lightweight and extensible

---

## Language and Naming Conventions

| Convention | Rule |
|------------|------|
| **Language** | Python >= 3.12 |
| **Package name** | `k` (lowercase) |
| **Module names** | `snake_case` (e.g., `rigid_body.py`) |
| **Class names** | `PascalCase` (e.g., `PhysicalObject`) |
| **Function names** | `snake_case` (e.g., `apply_force`) |
| **Constants** | `UPPER_SNAKE_CASE` |
| **Type aliases** | `PascalCase` ending in `T` (e.g., `Vector3T`) |
| **Private members** | Prefix with `_` (e.g., `_internal_state`) |

## Dependency Management

Dependencies are managed with **Poetry**.

| Command | Description |
|---------|-------------|
| `poetry install` | Install all dependencies |
| `poetry add <pkg>` | Add core dependency |
| `poetry add --group dev <pkg>` | Add development dependency |
| `poetry add --group viz <pkg>` | Add visualization dependency |
| `poetry add --group optional <pkg>` | Add optional dependency |
| `poetry shell` | Activate virtual environment |
| `poetry run <cmd>` | Run command in virtual environment |

Dependency groups:
- **main**: Core dependencies (numpy, scipy)
- **viz**: Visualization (matplotlib, pyvista, pillow)
- **dev**: Development tools (pytest, black, sphinx, etc.)
- **optional**: Optional features (manim, numba, h5py, etc.)

---

## Tech Stack

Managed via Poetry (`pyproject.toml`).

| Component | Library | Version |
|-----------|---------|---------|
| **Dependency manager** | **Poetry** | **latest** |
| Core computation | NumPy | ^2.4.4 |
| Scientific computing | SciPy | >=1.7 |
| 2D visualization | Matplotlib | ^3.10.9 |
| 3D visualization | PyVista | ^0.47.3 |
| Animation | Manim | ^0.20.1 |
| Documentation | Sphinx | ^9.1.0 |
| Testing | pytest | ^9.0.3 |
| Code formatting | Black | ^26.3.1 |

---

## Coding Guidelines

1. **[Modularity]** — Each function does one thing only. No multi-purpose functions.
2. **[Type hints]** — All public functions must have type hints. Use `Vector3T = NDArray[np.float64]` for 3D vectors and `numpy.typing.NDArray` for array inputs.
3. **[No comments]** — Do not add comments unless explicitly required by user.
4. **[Lazy imports]** — Heavy dependencies (viz) imported only when needed.
5. **[Pure Python core]** — Build physics calculations from scratch; import external libs only when necessary.
6. **[Plugin architecture]** — Physics domains must implement `PhysicsPlugin` protocol.
7. **[Data classes]** — Use `@dataclass` for all state/representation objects.

---

## Documentation Standards

- Every module must have a corresponding `AGENTS-[module].md` file.
- Every class must have a docstring with Args, Returns, Raises.
- Public API functions must have Google-style docstrings.
- Examples in docstrings must be complete and runnable.

---

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation
- `test:` — Tests
- `refactor:` — Code refactoring
- `chore:` — Maintenance

Example: `feat: add Force class to mechanics module`

---

## What to Avoid

- Do not import heavy FOSS physics engines (PyChrono, DART, Newton) unless explicitly requested
- Do not add unnecessary dependencies beyond core stack
- Do not create monolithic classes that handle multiple concerns
- Do not skip type hints on new functions
- Do not write inline comments explaining obvious code

---

## Module-Level AGENTS Files

| Module | AGENTS File | Status |
|--------|-------------|--------|
| core | `k/core/AGENTS-core.md` | Template |
| physics (parent) | `k/physics/AGENTS-physics.md` | Template |
| physics/mechanics | `k/physics/mechanics/AGENTS-mechanics.md` | Template |
| physics/thermodynamics | `k/physics/thermodynamics/AGENTS-thermodynamics.md` | Template |
| physics/electromagnetism | `k/physics/electromagnetism/AGENTS-electromagnetism.md` | Template |
| physics/optics | `k/physics/optics/AGENTS-optics.md` | Template |
| physics/fluid | `k/physics/fluid/AGENTS-fluid.md` | Template |
| solver | `k/solver/AGENTS-solver.md` | Template |
| calc | `k/calc/AGENTS-calc.md` | Template |
| viz | `k/viz/AGENTS-viz.md` | Template |
| utils | `k/utils/AGENTS-utils.md` | Template |

---

## Dependency and Inheritance Map

```
Root AGENTS.md (global rules)
    │
    ├── k/core/AGENTS-core.md
    ├── k/physics/AGENTS-physics.md (parent)
    │   ├── k/physics/mechanics/AGENTS-mechanics.md
    │   ├── k/physics/thermodynamics/AGENTS-thermodynamics.md
    │   ├── k/physics/electromagnetism/AGENTS-electromagnetism.md
    │   ├── k/physics/optics/AGENTS-optics.md
    │   └── k/physics/fluid/AGENTS-fluid.md
    ├── k/solver/AGENTS-solver.md
    ├── k/calc/AGENTS-calc.md
    ├── k/viz/AGENTS-viz.md
    └── k/utils/AGENTS-utils.md

Local rules override global rules. Module-level files focus on domain-specific behavior, constraints, and invariants.
```

---

## Project Structure Reference

```
K/
├── k/                          # Main package
│   ├── __init__.py
│   ├── core/                   # Core abstractions
│   │   ├── space.py
│   │   ├── object.py
│   │   ├── subsystem.py
│   │   ├── state.py
│   │   └── plugin.py
│   ├── physics/                # Physics domains
│   │   ├── mechanics/
│   │   ├── thermodynamics/
│   │   ├── electromagnetism/
│   │   ├── optics/
│   │   └── fluid/
│   ├── solver/                 # Simulation engine
│   ├── calc/                   # Calculation utilities
│   ├── viz/                    # Visualization
│   └── utils/                  # Utilities
├── tests/
├── docs/man/
├── dev/plans/
└── AGENTS.md (this file)
```
