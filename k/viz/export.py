from __future__ import annotations

from typing import Any

from k.viz.base import RenderConfig


class ExportManager:
    def __init__(self, config: RenderConfig | None = None) -> None:
        self.config = config or RenderConfig()

    def export_png(self, render_output: Any, path: str) -> None:
        from PIL import Image

        render_output.savefig(path, format="png", dpi=100)

    def export_svg(self, render_output: Any, path: str) -> None:
        render_output.savefig(path, format="svg")

    def export_frames_to_gif(self, frames: list[Any], path: str, fps: int = 30) -> None:
        from PIL import Image
        import io

        images = []
        for f in frames:
            if isinstance(f, str):
                images.append(Image.open(f))
            elif hasattr(f, "savefig"):
                buf = io.BytesIO()
                f.savefig(buf, format="png", dpi=100)
                buf.seek(0)
                images.append(Image.open(buf))
            else:
                images.append(f)
        if images:
            images[0].save(
                path,
                save_all=True,
                append_images=images[1:],
                duration=1000 // fps,
                loop=0,
            )

    def export_frames_to_mp4(self, frames: list[Any], path: str, fps: int = 30) -> None:
        import subprocess

        temp_dir = path + "_temp"
        import os

        os.makedirs(temp_dir, exist_ok=True)
        for i, frame in enumerate(frames):
            frame.save(f"{temp_dir}/frame_{i:04d}.png")
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                str(fps),
                "-i",
                f"{temp_dir}/frame_%04d.png",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                path,
            ],
            check=True,
        )
        for f in os.listdir(temp_dir):
            os.remove(f"{temp_dir}/{f}")
        os.rmdir(temp_dir)
