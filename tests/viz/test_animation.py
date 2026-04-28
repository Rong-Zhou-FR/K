from __future__ import annotations

import numpy as np
from k.viz.animation import Animation
from k.viz.base import RenderConfig
from k.core.state import State
from k.core.object import PhysicalObject
from k.core.space import Space


class MockSolver:
    def step(self, space: Space, dt: float) -> None:
        for obj in space.objects.values():
            obj.state.position += obj.state.velocity * dt


def test_animation_init() -> None:
    anim = Animation(frames=50, fps=60)
    assert anim.frames == 50
    assert anim.fps == 60


def test_animation_custom_config() -> None:
    config = RenderConfig()
    anim = Animation(frames=200, fps=24, config=config)
    assert anim.frames == 200
    assert anim.fps == 24


def test_animation_create_from_solver_matplotlib(tmp_path) -> None:
    anim = Animation(frames=10, fps=10)
    state = State(
        position=np.array([0, 0, 0], dtype=np.float64),
        velocity=np.array([1, 0, 0], dtype=np.float64),
        acceleration=np.zeros(3, dtype=np.float64),
        orientation=np.array([1, 0, 0, 0], dtype=np.float64),
        angular_velocity=np.zeros(3, dtype=np.float64),
        mass=1.0,
        inertia=np.eye(3, dtype=np.float64),
    )
    obj = PhysicalObject(shape="point", state=state, id="obj1")
    space = Space(dimensions=2)
    space.add(obj)
    solver = MockSolver()
    output = str(tmp_path / "test.gif")
    anim.create_from_solver(
        space, solver, duration=1.0, output_path=output, renderer_type="matplotlib"
    )
    assert len(space.objects) > 0


def test_animation_manim_raises_without_manim() -> None:
    anim = Animation()
    try:
        import manim  # noqa: F401

        result = anim._create_manim_animation([])
        assert result is not None
    except ImportError:
        try:
            anim._create_manim_animation([])
        except RuntimeError as e:
            assert "manim" in str(e)
            return
        assert False
