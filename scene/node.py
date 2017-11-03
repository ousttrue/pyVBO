import lah


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
    def __init__(self, name: str, shader, mesh):
        super().__init__(name)
        self.type = 'geometry'
        self.shader = shader
        self.mesh = mesh
        #self.angle = 0
        #self.anglular_velocity = 20 * lah.TO_RADIANS

    def update(self, delta):
        #self.angle+=self.anglular_velocity * d * 0.001
        #self.model = lah.Mat4.rotateZAxisByRadians(self.angle)
        pass

    def render(self, context):
        self.shader.use()
        self.shader.set_uniform_mat4('M', context.model.array)
        self.shader.set_uniform_mat4('V', context.view.array)
        self.shader.set_uniform_mat4('VM', context.mv.array)
        self.shader.set_uniform_mat4('PVM', context.mvp.array)
        self.shader.set_uniform_vec3('LightDir', context.lightDir.array)
        if self.mesh.texture:
            self.shader.set_uniform_texture('Tex0', 0)
        self.mesh.render()


class SceneContext:
    def __init__(self, camera, lightDir):
        self.camera = camera
        self.lightDir = lightDir
        self._view = None
        self._model = None
        self._mv = None
        self._mvp = None
        self.set_model(None)

    def set_model(self, transform):
        self.transform = transform
        self._mv = None
        self._mvp = None
        self._model = None

    @property
    def model(self):
        if not self._model:
            self._model = self.transform.mat4
        return self._model

    @property
    def view(self):
        if not self._view:
            self._view = self.camera.view
        return self._view

    @property
    def mv(self):
        if not self._mv:
            self._mv = self.model * self.view
        return self._mv

    @property
    def mvp(self):
        if not self._mvp:
            self._mvp = self.mv * self.camera.projection
        return self._mvp
