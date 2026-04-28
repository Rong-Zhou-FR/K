from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from k.core.object import PhysicalObject
    from k.core.plugin import PhysicsPlugin


class Space:
    def __init__(
        self,
        dimensions: int = 3,
        domains: list[str] | None = None,
    ) -> None:
        if dimensions not in (2, 3):
            raise ValueError("dimensions must be 2 or 3")
        self.dimensions = dimensions
        self.objects: dict[str, PhysicalObject] = {}
        self.enabled_domains: set[str] = set(domains or ["mechanics"])
        self._plugins: dict[str, PhysicsPlugin] = {}

    def add(self, obj: PhysicalObject) -> None:
        if obj.id in self.objects:
            raise ValueError(f"Object with id {obj.id!r} already exists in space")
        self.objects[obj.id] = obj
        for domain in self.enabled_domains:
            obj.state.enabled_domains.add(domain)

    def remove(self, obj_id: str) -> None:
        self.objects.pop(obj_id, None)

    def enable_domain(self, domain: str) -> None:
        self.enabled_domains.add(domain)
        for obj in self.objects.values():
            obj.state.enabled_domains.add(domain)

    def disable_domain(self, domain: str) -> None:
        self.enabled_domains.discard(domain)
        for obj in self.objects.values():
            obj.state.enabled_domains.discard(domain)

    def register_plugin(self, plugin: PhysicsPlugin) -> None:
        plugin.initialize(self)
        self._plugins[plugin.name] = plugin

    def __repr__(self) -> str:
        return f"Space(dimensions={self.dimensions}, objects={len(self.objects)})"
