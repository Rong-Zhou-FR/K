# AGENTS-viz.md — Visualization Agent Instructions

## Summary

Visualization module: 2D/3D rendering, animation, and diagrams.

## Purpose and Expected Behavior

Rendering for all physics domains:
- 2D visualization (matplotlib)
- 3D visualization (pyvista)
- Animation generation
- Domain-specific diagrams (force, optical)

## Constraints and Invariants

- Lazy imports: viz modules imported only when rendering
- Support both static images and animations
- Export formats: PNG, SVG, MP4, GIF
- Resolution configurable

## Key Classes

```python
class Renderer(ABC):
    @abstractmethod
    def render(self, space: Space) -> Any: ...

class Matplotlib2D(Renderer):
    # 2D visualization

class PyVista3D(Renderer):
    # 3D visualization

class ForceDiagram:
    # Draw force vectors on objects

class OpticalDiagram:
    # Draw ray paths, lenses, mirrors
```

## Documentation Reference

- `docs/man/viz/index.md`
- `docs/man/viz/2d.md`
- `docs/man/viz/3d.md`
- `docs/man/viz/diagrams.md`

## Domain-Specific Rules for Agents

- Use lazy imports for heavy viz deps
- Support multiple camera angles (3D)
- Color coding by domain (optional)
- Animate time evolution
