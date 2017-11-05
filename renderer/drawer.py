# pylint: disable=W0401,W0614,W0621,W0622
from logging import getLogger
logger = getLogger(__name__)

from OpenGL.GL import *

from .vbo import VBO
from .texture import Texture
from .vertexbuffer import Topology, AttributeLayout, Semantics
from .rendercontext import RenderContext
from .glsl import ShaderProgram
from pyvbo import pmd
from PIL import Image


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
    def from_pmd(model: pmd.Model, shader:ShaderProgram):
        self = Drawer()
        self.indices = VBO(model.indices)
        self.vertices = VBO(model.vertices, GL_FLOAT)
        self.layout = shader.vertex_layout
        self.stride = shader.vertex_stride
        self.topology = GL_TRIANGLES

        def create_submesh(material):
            texture = Texture()
            if material.texture:
                texture_name = material.texture.decode('cp932')
                if '*' in texture_name:
                    texture_name, _ = texture_name.split('*', 1)
                texture_file = model.metadata.base_path / texture_name
                if texture_file.exists():
                    logger.debug("%s exists", texture_file)
                    with texture_file.open('rb') as f:
                        image = Image.open(f)
                        image = image.convert('RGBA')
                    texture.create_texture(
                        image.width, image.height, image.tobytes())
                else:
                    logger.warning("%s not exists", texture_file)
            return SubMesh(shader, material.index_count, material.color, texture)
        self.submeshes = [create_submesh(x) for x in model.materials]        
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
