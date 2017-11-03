# pylint: disable=W0401,W0614,W0621,W0622
from OpenGL.GL import *

from .vbo import VBO
from .texture import Texture


class Drawer:
    def __init__(self, builder):
        self.indices = VBO(builder.indices)
        self.vertices = VBO(builder.vertices)
        self.layout = builder.layout
        self.stride = builder.stride
        self.vao = None
        self.texture = Texture()

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

        self.indices.drawIndex()
