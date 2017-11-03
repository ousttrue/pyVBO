# pylint: disable=W0401,W0614,W0621,W0622
import logging
logger = logging.getLogger(__name__)

import pathlib
from OpenGL.GL import *
from OpenGL.GLU import *

import lah
from renderer import AttributeLayout, Semantics, Drawer, ShaderProgram, MeshBuilder
from .camera import Camera
from .node import MeshNode, SceneContext

vertex_layout = (
    AttributeLayout(Semantics.POSITION, 'f', 3),
    AttributeLayout(Semantics.NORMAL, 'f', 3),
    AttributeLayout(Semantics.COLOR, 'f', 4),
    AttributeLayout(Semantics.TEXCOORD, 'f', 2)
)

VS = (pathlib.Path(__file__).parent / 'shader.vert').read_text()
FS = (pathlib.Path(__file__).parent / 'shader.frag').read_text()


class Scene:
    """
    [CLASSES] Controllerクラスは、glglueの規約に沿って以下のコールバックを実装する
    """

    def __init__(self):
        self.is_initialized = False
        self.mouseRight = False
        self.mouseMiddle = False
        self.mouseLeft = False
        self.mouseX = 0
        self.mouseY = 0
        self.mouseFirst = True
        self.camera = Camera()
        self.clear_color = (0.0, 0.0, 1.0, 0.0)

        self.shader = ShaderProgram(VS, FS)
        self.lightDir = lah.Vec3(1, -3, 10).normalized

        builder = MeshBuilder(vertex_layout)
        builder.create_cube(0.5)
        mesh = Drawer(builder)
        self.nodes = []
        self.nodes.append(MeshNode('cube', self.shader, mesh))

    def onResize(self, w: int, h: int):
        glViewport(0, 0, w, h)
        self.camera.resize(w, h)

    def onLeftDown(self, x, y):
        #logger.debug('onLeftDown: %d, %d', x, y)
        pass

    def onLeftUp(self, x, y):
        #logger.debug('onLeftUp: %d, %d', x, y)
        pass

    def onMiddleDown(self, x, y):
        self.mouseMiddle = True
        self.mouseX = x
        self.mouseY = y

    def onMiddleUp(self, x, y):
        self.mouseMiddle = False
        self.mouseX = x
        self.mouseY = y

    def onRightDown(self, x, y):
        self.mouseRight = True
        self.mouseX = x
        self.mouseY = y

    def onRightUp(self, x, y):
        self.mouseRight = False
        self.mouseX = x
        self.mouseY = y

    def onMotion(self, x, y):
        dx = x - self.mouseX
        dy = y - self.mouseY
        #logger.debug("onMotion %d x %d => %d x %d", x, y, dx, dy)
        self.mouseX = x
        self.mouseY = y
        if self.mouseFirst:
            self.mouseFirst = False
            return

        if self.mouseMiddle:
            self.camera.shift(dx, dy)

        if self.mouseRight:
            self.camera.yaw_pitch(dx, dy)

    def onWheel(self, d):
        self.camera.dolly(d)

    def onKeyDown(self, keycode):
        logger.debug('onKeyDown: %d', keycode)

    def update(self, delta):
        pass

    def initialize(self):
        logger.info(glGetString(GL_VERSION))
        logger.info(glGetString(GL_SHADING_LANGUAGE_VERSION))
        logger.info('OpenGL%d.%d', glGetInteger(
            GL_MAJOR_VERSION), glGetInteger(GL_MINOR_VERSION))
        # self.scene.initialize()

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        self.is_initialized = True

    def draw(self):
        if not self.is_initialized:
            self.initialize()

        # clear
        glClearColor(*self.clear_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # render
        context = SceneContext(self.camera, self.lightDir)
        for x in self.nodes:
            context.set_model(x.model)
            x.render(context)
