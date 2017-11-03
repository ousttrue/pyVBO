import lah

MOUSE_ROTATE_PER_PIXEL = 0.3
MOUSE_SHIFT_FACTOR = 2


class Camera:
    def __init__(self):
        self.reset()
        self._pitch = 0
        self.width = 0
        self.height = 0
        self._projection = lah.Mat4.identity()

    def reset(self):
        self._d = 3
        self._yaw = 0
        self._pitch = 0
        self._shiftX = 0
        self._shiftY = 0
        self.width = 1
        self.height = 1

    def resize(self, w, h):
        #logger.debug('onResize: %d, %d', w, h)
        aspect = w / h
        #self._projection = lah.Mat4.perspective_lh(30.0, aspect, 1.0, 40.00)
        self._projection = lah.Mat4.pinhole(30.0, aspect, 1.0, 40.0)
        #self._projection = lah.Mat4.orthognonal(-2, 2, -2, 2, 0, 4)
        self.width = w
        self.height = h

    @property
    def projection(self):
        return self._projection

    @property
    def view(self):
        return (
            lah.Mat4.rotateYAxisByDegrees(self._yaw)
            * lah.Mat4.rotateXAxisByDegrees(self._pitch)
            #* lah.Mat4.translate(self._shiftX, self._shiftY, -self._d)
            * lah.Mat4.translate(self._shiftX, self._shiftY, self._d)
        )

    def yaw_pitch(self, x, y):
        self._yaw -= (x * MOUSE_ROTATE_PER_PIXEL)
        self._pitch -= (y * MOUSE_ROTATE_PER_PIXEL)
        if self._pitch > 90:
            self._pitch = 90
        elif self._pitch < -90:
            self._pitch = -90

    def shift(self, x, y):
        if self.width == 0 or self.height == 0:
            return
        self._shiftX += (x / self.width * MOUSE_SHIFT_FACTOR * self._d)
        self._shiftY -= (y / self.height * MOUSE_SHIFT_FACTOR * self._d)
        #logger.debug("shift %f x %f", self._shiftX, self._shiftY)

    def dolly(self, d):
        if d > 0:
            self._d *= 1.1
        elif d < 0:
            self._d *= 0.9
