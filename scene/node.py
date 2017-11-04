import lah
from renderer import Drawer


class Node:
    def __init__(self, name: str):
        self.name = name
        self.type = 'UNKNOWN'
        self.model = lah.Transform.identity()

    def set_position(self, x, y, z):
        self.model.pos = lah.Vec3(x, y, z)

    def set_quaternion(self, x, y, z, w):
        self.model.rot = lah.Quaternion(x, y, z, w)

    def update(self, delta):
        pass


class MeshNode(Node):
    def __init__(self, name: str, mesh: Drawer):
        super().__init__(name)
        self.type = 'geometry'
        self.mesh = mesh

    def update(self, delta):
        '''
        animation
        '''
        pass

    def render(self, context):
        self.mesh.render(context)
