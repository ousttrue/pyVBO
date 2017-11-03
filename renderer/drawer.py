# pylint: disable=W0401,W0614,W0621,W0622
from logging import getLogger, Handler, DEBUG, WARNING, ERROR
logger = getLogger(__name__)

from OpenGL.GL import *

from .vbo import VBO
from .texture import Texture
from .vertexbuffer import Topology, AttributeLayout, Semantics


pmd_vertex_layout = (
    AttributeLayout(Semantics.POSITION, 'f', 3),
    AttributeLayout(Semantics.NORMAL, 'f', 3),
    AttributeLayout(Semantics.TEXCOORD, 'f', 2)
)
pmd_vertex_stride = 38


class Drawer:
    def __init__(self):
        self.indices = None
        self.vertices = None
        self.layout = None
        self.stride = 0
        self.vao = None
        self.texture = None
        self.topology = None

    @staticmethod
    def from_builder(builder):
        self = Drawer()
        self.indices = VBO(builder.indices)
        self.vertices = VBO(builder.vertices)
        self.layout = builder.layout
        self.stride = builder.stride
        self.texture = Texture()

        if builder.topology == Topology.Triangle:
            self.topology = GL_TRIANGLES
        elif builder.topology == Topology.Line:
            self.topology = GL_LINES
        else:
            raise Exception("unknown topology")

        return self

    @staticmethod
    def from_pmd(pmd):
        self = Drawer()
        self.indices = VBO(pmd.indices)
        self.vertices = VBO(pmd.vertices, GL_FLOAT)
        self.layout = pmd_vertex_layout
        self.stride = pmd_vertex_stride
        self.texture = Texture()
        self.topology = GL_TRIANGLES
        return self

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
