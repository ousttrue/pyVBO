from abc import ABCMeta, abstractmethod
from typing import List

import lah
from renderer import Drawer, RenderContext


class ComponentBase(metaclass=ABCMeta):
    @abstractmethod
    def update(self, now: float)->None:
        pass

    @abstractmethod
    def render(self, context: RenderContext)->None:
        pass


class Node:
    def __init__(self, name: str)->None:
        self.name = name
        self.model = lah.Transform.identity()
        self.components: List[ComponentBase] = []

    def set_position(self, x: float, y: float, z: float)->None:
        self.model.pos = lah.Vec3(x, y, z)

    def set_quaternion(self, x: float, y: float, z: float, w: float)->None:
        self.model.rot = lah.Quaternion(x, y, z, w)

    def update(self, now: float)->None:
        for x in self.components:
            x.update(now)

    def render(self, context: RenderContext)->None:
        for x in self.components:
            x.render(context)


class MeshComponent(ComponentBase):
    def __init__(self, mesh: Drawer)->None:
        self.mesh = mesh

    def update(self, now: float):
        pass

    def render(self, context: RenderContext):
        self.mesh.render(context)
