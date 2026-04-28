from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from k.core.object import PhysicalObject


class Subsystem:
    def __init__(self, name: str) -> None:
        self.name = name
        self.objects: list[PhysicalObject] = []

    def add(self, obj: PhysicalObject) -> None:
        if obj not in self.objects:
            self.objects.append(obj)

    def remove(self, obj: PhysicalObject) -> None:
        if obj in self.objects:
            self.objects.remove(obj)

    def __repr__(self) -> str:
        return f"Subsystem(name={self.name!r}, objects={len(self.objects)})"
