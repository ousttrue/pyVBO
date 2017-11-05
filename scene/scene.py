# pylint: disable=W0401,W0614,W0621,W0622
import logging
logger = logging.getLogger(__name__)

import pathlib
from OpenGL.GL import *
from OpenGL.GLU import *

import lah
from renderer import Drawer, ShaderProgram, MeshBuilder, Camera, RenderContext
from .node import MeshNode

import shaders


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

        self.gizmo_shader = shaders.GizmoShader
        self.lightDir = lah.Vec3(1, -3, 10).normalized

        self.gizmos = []
        self.nodes = []

        # grid
        builder = MeshBuilder(self.gizmo_shader.vertex_layout)
        builder.create_grid(1, 5)
        mesh = Drawer.from_builder(builder)
        mesh.create_submesh(self.gizmo_shader)
        self.gizmos.append(MeshNode('grid', mesh))

    def add_mesh(self, name, mesh: Drawer):
        self.nodes.clear()
        self.nodes.append(MeshNode(name, mesh))

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
        context = RenderContext(self.camera, self.lightDir)

        for x in self.gizmos:
            context.set_model(x.model)
            x.render(context)

        for x in self.nodes:
            context.set_model(x.model)
            x.render(context)
