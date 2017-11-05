# pylint: disable=W0401,W0614,W0621,W0622
import logging
logger = logging.getLogger(__name__)

from OpenGL.GL import *
from OpenGL.GLU import *

import lah
from renderer import Drawer, MeshBuilder, Camera, RenderContext
import shaders
from observable_property import Prop, ListProp, RGBAf

from .node import Node, MeshComponent


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
        self.background_color = Prop[RGBAf](RGBAf(0.3, 0.3, 0.5, 0.0))

        #
        # gizmos
        #
        self.gizmos = ListProp[Node]()
        self.gizmo_shader = shaders.GizmoShader

        # axis
        builder = MeshBuilder(self.gizmo_shader.vertex_layout)
        builder.create_axis(5)
        axis_mesh = Drawer.from_builder(builder, self.gizmo_shader)
        axis_node = Node('axis')
        axis_node.model.pos=lah.Vec3(0, 0.001, 0)
        axis_node.components.append(MeshComponent(axis_mesh))
        self.gizmos.append(axis_node)

        # grid
        builder = MeshBuilder(self.gizmo_shader.vertex_layout)
        builder.create_grid(1, 5)
        grid_mesh = Drawer.from_builder(builder, self.gizmo_shader)
        grid_node = Node('grid')
        grid_node.components.append(MeshComponent(grid_mesh))
        self.gizmos.append(grid_node)

        # camera
        self.camera = Camera()
        camera_node = Node('camera')
        self.gizmos.append(camera_node)

        # light
        self.lightDir = lah.Vec3(1, -3, 10).normalized
        light_node = Node('light')
        self.gizmos.append(light_node)

        #
        # nodes
        #
        self.nodes = ListProp[Node]()

    def add_mesh(self, name, mesh: Drawer):
        mesh_node = Node(name)
        mesh_node.components.append(MeshComponent(mesh))
        self.nodes.reset(mesh_node)

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
        background_color = self.background_color.value
        glClearColor(background_color.red, background_color.green,
                     background_color.blue, background_color.alpha)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #
        # update
        #

        #
        # render
        #
        context = RenderContext(self.camera, self.lightDir)

        for x in self.gizmos.values:
            context.set_model(x.model)
            x.render(context)

        for x in self.nodes.values:
            context.set_model(x.model)
            x.render(context)
