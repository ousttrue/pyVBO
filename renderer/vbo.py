from logging import getLogger, Handler, DEBUG, WARNING, ERROR
logger = getLogger(__name__)


from OpenGL.GL import *
from OpenGL.GLU import *
import ctypes


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
    # array.array
    def __init__(self, array):
        self.vbo = None
        self.array = array
        self.gltype = to_gltype(array.typecode)

    def initialize(self):
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        addr, count = self.array.buffer_info()
        glBufferData(GL_ARRAY_BUFFER, self.array.itemsize *
                     len(self.array), ctypes.c_void_p(addr), GL_STATIC_DRAW)
        # (ctypes.c_float*len(self.vertices))(*self.vertices)

    def setAttrib(self, slot, layout, stride):
        glEnableVertexAttribArray(slot)
        #glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexAttribPointer(slot,
                              layout.value_elements,
                              to_gltype(layout.value_type),
                              False,
                              stride,
                              ctypes.c_void_p(layout.offset)
                              )

    def setIndex(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo)

    def drawIndex(self, topology):
        glDrawElements(topology, len(self.array), self.gltype, None)
