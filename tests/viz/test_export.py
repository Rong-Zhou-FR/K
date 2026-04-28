from __future__ import annotations

import numpy as np
from k.viz.export import ExportManager
from k.viz.base import RenderConfig


def test_export_manager_init() -> None:
    em = ExportManager()
    assert em.config is not None


def test_export_manager_custom_config() -> None:
    config = RenderConfig(resolution=(800, 600))
    em = ExportManager(config)
    assert em.config.resolution == (800, 600)


def test_export_png(tmp_path) -> None:
    import matplotlib.pyplot as plt

    em = ExportManager()
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    output = str(tmp_path / "test.png")
    em.export_png(fig, output)
    plt.close(fig)
    import os

    assert os.path.exists(output)


def test_export_svg(tmp_path) -> None:
    import matplotlib.pyplot as plt

    em = ExportManager()
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    output = str(tmp_path / "test.svg")
    em.export_svg(fig, output)
    plt.close(fig)
    import os

    assert os.path.exists(output)


def test_export_frames_to_gif(tmp_path) -> None:
    from PIL import Image

    em = ExportManager()
    frames = [Image.new("RGB", (100, 100), color="red") for _ in range(5)]
    output = str(tmp_path / "test.gif")
    em.export_frames_to_gif(frames, output)
    import os

    assert os.path.exists(output)


def test_export_frames_to_mp4_missing_ffmpeg(tmp_path) -> None:
    from PIL import Image

    em = ExportManager()
    frames = [Image.new("RGB", (100, 100), color="red") for _ in range(5)]
    output = str(tmp_path / "test.mp4")
    try:
        em.export_frames_to_mp4(frames, output)
    except Exception:
        pass
