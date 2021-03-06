# pylint: disable=W0401,W0614,W0621,W0622
import logging
logger = logging.getLogger(__name__)

import sys
from OpenGL.GLU import *
from OpenGL.GL import *


def printOpenGLError():
    err = glGetError()
    if err != GL_NO_ERROR:
        logger.error('GLERROR: %s', gluErrorString(err))
        sys.exit()


def compileShader(source, shaderType):
    """Compile shader source of given type"""
    shader = glCreateShader(shaderType)
    glShaderSource(shader, [source])
    # printOpenGLError()
    glCompileShader(shader)
    # printOpenGLError()
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if result == GL_FALSE:
        msg = glGetShaderInfoLog(shader)
        if msg:
            logger.error(msg)
    return shader


class ShaderProgram:
    def __init__(self, vs_source, fs_source, vertex_layout, vertex_stride=None):
        self.vs_source = vs_source
        self.fs_source = fs_source
        self.program = None
        self.is_initialized = False
        self.uniform_map = {}
        self.vertex_layout = vertex_layout
        self.vertex_stride = vertex_stride

    def initialize(self):
        logger.info('create program')
        self.program = glCreateProgram()
        vs = compileShader(self.vs_source, GL_VERTEX_SHADER)
        glAttachShader(self.program, vs)
        fs = compileShader(self.fs_source, GL_FRAGMENT_SHADER)
        glAttachShader(self.program, fs)

        glLinkProgram(self.program)
        # printOpenGLError()
        result = glGetProgramiv(self.program, GL_LINK_STATUS)
        if result == GL_FALSE:
            msg = glGetProgramInfoLog(self.program)
            if msg:
                logger.error(msg)

        self.is_initialized = True

    def use(self):
        if not self.is_initialized:
            self.initialize()
        glUseProgram(self.program)

    def get_uniform(self, name):
        if name in self.uniform_map:
            return self.uniform_map[name]
        else:
            id = glGetUniformLocation(self.program, name)
            if id < 0:
                return
            self.uniform_map[name] = id
            return id

    def set_uniform_texture(self, name, slot):
        loc = self.get_uniform(name)
        if loc is not None:
            glUniform1i(loc, slot)

    def set_uniform_vec3(self, name, value):
        loc = self.get_uniform(name)
        if loc is not None:
            glUniform3fv(loc, 1, value)

    def set_uniform_vec4(self, name, value):
        loc = self.get_uniform(name)
        if loc is not None:
            glUniform4fv(loc, 1, value)

    def set_uniform_mat3(self, name, value):
        id = glGetUniformLocation(self.program, name)
        if id is not None:
            glUniformMatrix3fv(id, 1, GL_FALSE, value)

    def set_uniform_mat4(self, name, value):
        id = glGetUniformLocation(self.program, name)
        if id is not None:
            glUniformMatrix4fv(id, 1, GL_FALSE, value)
