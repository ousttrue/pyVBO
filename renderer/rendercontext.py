
class RenderContext:
    def __init__(self, camera, lightDir):
        self.camera = camera
        self.lightDir = lightDir
        self._view = None
        self._model = None
        self._mv = None
        self._mvp = None
        self.set_model(None)
        self.color=(1, 1, 1, 1)

    def set_model(self, transform):
        self.transform = transform
        self._mv = None
        self._mvp = None
        self._model = None

    def set_submesh(self, color):
        self.color = color

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
