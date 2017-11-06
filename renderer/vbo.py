# pylint: disable=W0401,W0614,W0621,W0622
from logging import getLogger
logger = getLogger(__name__)

import array
import ctypes
import struct
from typing import List

from OpenGL.GL import *
from OpenGL.GLU import *

from .vertexbuffer import AttributeLayout


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


class VBOBase:
    def __init__(self)->None:
        self.vbo = None
        self.stride = 0
        self.layouts: List[AttributeLayout] = []

    def initialize(self):
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

    def set_layouts(self, layouts: List[AttributeLayout], stride: int):
        self.stride = stride
        self.layouts = layouts[:]
        for slot, layout in enumerate(layouts):
            glEnableVertexAttribArray(slot)
            #glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glVertexAttribPointer(slot,
                                  layout.value_elements,
                                  to_gltype(layout.value_type),
                                  False,
                                  stride,
                                  ctypes.c_void_p(layout.offset))


class CtypesVBO(VBOBase):
    def __init__(self, data: ctypes.Array)->None:
        super().__init__()
        self.data = data
        self.col_map = {i: x[0] for i, x in enumerate(data._type_._fields_)}

    def initialize(self):
        super().initialize()

        glBufferData(GL_ARRAY_BUFFER,
                     ctypes.sizeof(self.data._type_) * self.data._length_,
                     self.data, GL_STATIC_DRAW)

    @property
    def count(self):
        return len(self.data)

    def get(self, row, col):
        vertex = self.data[row]
        return getattr(vertex, self.col_map[col])


class ArrayVBO(VBOBase):
    def __init__(self, data: array.array)->None:
        super().__init__()
        self.data = data
        self.stride = None

    def initialize(self):
        super().initialize()

        addr, _ = self.data.buffer_info()
        glBufferData(GL_ARRAY_BUFFER,
                     self.data.itemsize * len(self.data),
                     ctypes.c_void_p(addr), GL_STATIC_DRAW)

    @property
    def count(self):
        return (len(self.data) * self.data.itemsize) / self.stride

    def get(self, row: int, col: int):
        assert self.data.typecode == 'B'
        layout = self.layouts[col]
        offset = self.stride * row + layout.offset
        data = bytes(self.data[offset:offset + layout.size])
        return struct.unpack(layout.pack_format, data)


class ArrayVBOIndex(ArrayVBO):
    def __init__(self, data: array.array)->None:
        super().__init__(data)
        self.gltype = to_gltype(data.typecode)

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
