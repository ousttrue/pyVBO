# pylint: disable=W0401,W0614,W0621,W0622
from logging import getLogger, Handler, DEBUG, WARNING, ERROR
logger = getLogger(__name__)

from OpenGL.GL import *

from .vbo import VBO
from .texture import Texture
from .vertexbuffer import Topology


class Drawer:
    def __init__(self, builder):
        self.indices = VBO(builder.indices)
        self.vertices = VBO(builder.vertices)
        self.layout = builder.layout
        self.stride = builder.stride
        self.vao = None
        self.texture = Texture()

        if builder.topology == Topology.Triangle:
            self.topology = GL_TRIANGLES
        elif builder.topology == Topology.Line:
            self.topology = GL_LINES
        else:
            raise Exception("unknown topology")

    def initialize(self):
        self.indices.initialize()
        self.vertices.initialize()

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        for i, x in enumerate(self.layout):
            self.vertices.setAttrib(i, x, self.stride)
        self.indices.setIndex()

    def render(self):
        self.texture.bind()

        if not self.vao:
            self.initialize()

        glBindVertexArray(self.vao)

        self.indices.drawIndex(self.topology)
