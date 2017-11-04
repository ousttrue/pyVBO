# pylint: disable=W0401,W0614,W0621,W0622
from logging import getLogger
logger = getLogger(__name__)


import array
import ctypes
from OpenGL.GL import *
from OpenGL.GLU import *


def to_gltype(code):
    if code == 'f':
        return GL_FLOAT
    elif code == 'B':
        return GL_UNSIGNED_BYTE
    elif code == 'H':
        return GL_UNSIGNED_SHORT
    elif code == 'I':
        return GL_UNSIGNED_INT
    else:
        raise RuntimeError('unknown code: %s' % code)


class VBO:
    def __init__(self, data, gltype=None):
        self.vbo = None
        self.data = data
        if gltype:
            self.gltype = gltype
        else:
            self.gltype = to_gltype(data.typecode)

    def initialize(self):
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        if isinstance(self.data, array.array):
            addr, _ = self.data.buffer_info()
            glBufferData(GL_ARRAY_BUFFER,
                         self.data.itemsize * len(self.data),
                         ctypes.c_void_p(addr), GL_STATIC_DRAW)
        elif isinstance(self.data, ctypes.Array):
            glBufferData(GL_ARRAY_BUFFER,
                         ctypes.sizeof(self.data._type_) * self.data._length_,
                         self.data, GL_STATIC_DRAW)
        else:
            raise NotImplementedError()

    def setAttrib(self, slot, layout, stride):
        glEnableVertexAttribArray(slot)
        #glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexAttribPointer(slot,
                              layout.value_elements,
                              to_gltype(layout.value_type),
                              False,
                              stride,
                              ctypes.c_void_p(layout.offset))

    def setIndex(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo)

    def drawIndex(self, topology, offset=0, count=0):
        if count:
            glDrawElements(
                topology,
                count,
                self.gltype,
                ctypes.c_void_p(offset * self.data.itemsize))
        else:
            glDrawElements(
                topology,
                len(self.data),
                self.gltype,
                ctypes.c_void_p(0))
