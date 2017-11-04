# pylint: disable=W0401,W0614,W0621,W0622
from logging import getLogger
logger = getLogger(__name__)

from OpenGL.GL import *

from .vbo import VBO
from .texture import Texture
from .vertexbuffer import Topology, AttributeLayout, Semantics
from .rendercontext import RenderContext


pmd_vertex_layout = (
    AttributeLayout(Semantics.POSITION, 'f', 3),
    AttributeLayout(Semantics.NORMAL, 'f', 3),
    AttributeLayout(Semantics.TEXCOORD, 'f', 2)
)
pmd_vertex_stride = 38


class SubMesh:
    def __init__(self, shader, index_count, color, texture):
        self.shader = shader
        self.index_count = index_count
        self.color = color
        self.texture = texture

    def apply_shader(self, context: RenderContext):
        self.shader.use()
        self.shader.set_uniform_mat4('uM', context.model.array)
        self.shader.set_uniform_mat4('uV', context.view.array)
        self.shader.set_uniform_mat4('uVM', context.mv.array)
        self.shader.set_uniform_mat4('uPVM', context.mvp.array)
        self.shader.set_uniform_vec3('uLightDir', context.lightDir.array)
        if self.texture:
            self.texture.bind()
            self.shader.set_uniform_texture('uTex0', 0)
        self.shader.set_uniform_vec4('uColor', context.color)


class Drawer:
    def __init__(self):
        self.indices = None
        self.vertices = None
        self.layout = None
        self.stride = 0
        self.vao = None
        self.topology = None
        self.submeshes = []

    @staticmethod
    def from_builder(builder):
        self = Drawer()
        self.indices = VBO(builder.indices)
        self.vertices = VBO(builder.vertices)
        self.layout = builder.layout
        self.stride = builder.stride

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

    def get_texture(self, name: str):
        return None

    def create_submesh(self, shader):
        self.submeshes = [
            SubMesh(shader, len(self.indices.data), (1, 1, 1, 1), Texture())
        ]

    def render(self, context: RenderContext):
        if not self.vao:
            self.initialize()

        glBindVertexArray(self.vao)

        offset = 0
        for x in self.submeshes:
            # update material
            context.set_submesh(x.color)

            x.apply_shader(context)

            self.indices.drawIndex(self.topology, offset, x.index_count)
            offset += x.index_count
        #assert len(self.indices.data) == offset
