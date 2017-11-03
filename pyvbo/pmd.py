from logging import getLogger
logger = getLogger(__name__)

import ctypes
import array

from .bytesreader import BytesReader
from .metadata import MetaData, Direction, Coordinate


class Float2(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
    ]


class Float3(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
    ]


class Float4(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
        ("w", ctypes.c_float),
    ]


class Vertex(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("pos", Float3),
        ("normal", Float3),
        ("uv", Float2),
        ("bone0", ctypes.c_int16),
        ("bone1", ctypes.c_int16),
        ("weight0", ctypes.c_byte),
        ("flag", ctypes.c_byte),
    ]


assert ctypes.sizeof(Vertex) == 38


class Material(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('diffuse', Float4),
        ('specularity', ctypes.c_float),
        ('specular', Float3),
        ('ambient', Float3),
        ('toon_index', ctypes.c_byte),
        ('flag', ctypes.c_byte),
        ('index_count', ctypes.c_uint32),
        ('texture', ctypes.c_char * 20),
    ]


assert ctypes.sizeof(Material) == 70


class Model:
    def __init__(self, metadata, vertices, indices, materials):
        self.metadata = metadata
        self.vertices = vertices
        self.indices = indices
        self.materials = materials

    def __repr__(self):
        return f'{{Pmd {self.metadata.name}}}'


def load_bytes(data: bytes):
    # header
    r = BytesReader(data)
    if r.get_bytes(3) != b'Pmd':
        return None

    version = r.get_float()
    if version != 1.0:
        return None

    name = r.get_str(20, 'cp932')
    logger.debug(name)
    comment = r.get_str(256, 'cp932')
    logger.debug(comment)

    # vertices
    vertex_count = r.get_uint32()
    vertices_bytes = r.get_bytes(vertex_count * ctypes.sizeof(Vertex))
    vertices = (Vertex * vertex_count).from_buffer_copy(vertices_bytes)
    logger.debug('%d vertices. %d bytes', vertex_count, len(vertices))

    # indices
    index_count = r.get_uint32()
    indices = array.array('H')
    indices.frombytes(r.get_bytes(
        index_count * ctypes.sizeof(ctypes.c_uint16)))
    logger.debug('%d indices. %d bytes', index_count,
                 indices.itemsize * len(indices))

    # materials
    material_count = r.get_uint32()
    materials_bytes = r.get_bytes(material_count * ctypes.sizeof(Material))
    materials = (Material * material_count).from_buffer_copy(materials_bytes)
    logger.debug('%d materials. %d bytes', material_count, len(materials))

    metadata = MetaData(
        name, comment,
        Coordinate.YUP_ZFORWARD,
        Direction.Y_POSITIVE,
        Direction.Z_NEGATIVE,
        Direction.X_NEGATIVE,
        1.58 / 20
    )

    return Model(metadata, vertices, indices, materials)
