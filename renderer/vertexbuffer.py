import array
import struct
from enum import Enum
import lah


class Semantics(Enum):
    STRING = 0
    POSITION = 1
    NORMAL = 2
    COLOR = 3
    TEXCOORD = 4


class Topology(Enum):
    Triangle = 0
    Line = 1


def value_size(value_type):
    if value_type == 'f':
        return 4
    if value_type == 'H':
        return 2
    if value_type == 'I':
        return 4
    raise ValueError('unknown type: %s' % value_type)


class AttributeLayout:
    def __init__(self, semantics, value_type, value_elements, offset=None):
        self.semantics = semantics
        self.value_type = value_type
        self.value_elements = value_elements
        self.offset = offset

    @property
    def size(self):
        return value_size(self.value_type) * self.value_elements

    @property
    def pack_format(self):
        return self.value_type * self.value_elements


def create_format(layout):
    return "".join(("%d%s" % (x.value_elements, x.value_type) for x in layout))


class MeshBuilder:
    def __init__(self, layout, stride=None, topology=Topology.Triangle):
        self.indices = array.array('I')
        self.vertices = array.array('B')
        self.vertex_count = 0
        self.topology = topology

        offset = 0
        has_offset = False
        for x in layout:
            if x.offset:
                has_offset = True
            if not has_offset:
                x.offset = offset
            offset += x.size

        self.layout = layout

        if not stride:
            self.stride = 0
            for x in layout:
                self.stride += x.size

        self.fmt = create_format(layout)

        def init(self, *attribs):
            values = [item for sublist in attribs
                      for item in sublist]
            self.values = values

        self.Vertex = type('Vertex', (object,), {
            '__init__': init,
        })

    '''
    def reserve(self, vertex_count):
        self.vertices.extend(
            (0 for x in range(self.stride * vertex_count - len(self.vertices)))
            )
    '''

    def push_vertex(self, v):
        data = struct.pack(self.fmt, *v.values)
        self.vertices.extend(data)
        self.vertex_count += 1

    def push_line(self, begin, end):
        i = self.vertex_count

        self.push_vertex(begin)
        self.indices.append(i)

        self.push_vertex(end)
        self.indices.append(i + 1)

    def push_triangle(self, v0, v1, v2):
        i = self.vertex_count

        if not v0.values[3] or not v1.values[3] or not v2.values[3]:  # no normal
            # calc normal
            p0 = lah.Vec3(*v0.values[:3])
            p1 = lah.Vec3(*v1.values[:3])
            p2 = lah.Vec3(*v2.values[:3])
            v01 = p0 - p1
            v21 = p2 - p1
            normal = v01.normalized.cross(v21.normalized)
            v0.values[3:6] = normal.array
            v1.values[3:6] = normal.array
            v2.values[3:6] = normal.array

        self.push_vertex(v0)
        self.push_vertex(v1)
        self.push_vertex(v2)

        self.indices.append(i)
        self.indices.append(i + 1)
        self.indices.append(i + 2)

    def push_quad(self, v0, v1, v2, v3):
        self.push_triangle(v0, v1, v2)
        self.push_triangle(v2, v3, v0)

    def create_quad(self, s):
        self.push_quad(
            self.Vertex((-s, -s, 0), (0, 0, 1), (1, 1, 1, 1), (0, 0)),
            self.Vertex((s, -s, 0), (0, 0, 1), (1, 1, 1, 1), (1, 0)),
            self.Vertex((s, s, 0), (0, 0, 1), (1, 1, 1, 1), (1, 1)),
            self.Vertex((-s, s, 0), (0, 0, 1), (1, 1, 1, 1), (0, 1))
        )

    def create_axis(self, size: float):
        self.topology = Topology.Line
        self.push_line(
            self.Vertex((0, 0, 0), (0, 0, 0), (1, 0, 0, 1), (0, 0)),
            self.Vertex((size, 0, 0), (0, 0, 0), (1, 0, 0, 1), (0, 0))
        )
        self.push_line(
            self.Vertex((0, 0, 0), (0, 0, 0), (0, 1, 0, 1), (0, 0)),
            self.Vertex((0, size, 0), (0, 0, 0), (0, 1, 0, 1), (0, 0))
        )
        self.push_line(
            self.Vertex((0, 0, 0), (0, 0, 0), (0, 0, 1, 1), (0, 0)),
            self.Vertex((0, 0, size), (0, 0, 0), (0, 0, 1, 1), (0, 0))
        )

    def create_grid(self, delta: float, count: int):
        self.topology = Topology.Line
        size = delta * count
        for _x in range(-count, count + 1):
            x = _x * delta
            self.push_line(
                self.Vertex((x, 0, -size), (0, 1, 0), (1, 1, 1, 1), (0, 0)),
                self.Vertex((x, 0, size), (0, 1, 0), (1, 1, 1, 1), (0, 0)))
        for _z in range(-count, count + 1):
            z = _z * delta
            self.push_line(
                self.Vertex((-size, 0, z), (0, 1, 0), (1, 1, 1, 1), (0, 0)),
                self.Vertex((size, 0, z), (0, 1, 0), (1, 1, 1, 1), (0, 0)))

    def create_cube(self, s):
        v = [(-s, -s, s),
             (s, -s, s),
             (s, s, s),
             (-s, s, s),
             (-s, -s, -s),
             (s, -s, -s),
             (s, s, -s),
             (-s, s, -s)]
        c = [(0, 0, 0, 1),
             (1, 0, 0, 1),
             (0, 1, 0, 1),
             (0, 0, 1, 1),
             (0, 1, 1, 1),
             (1, 0, 1, 1),
             (1, 1, 1, 1),
             (1, 1, 0, 1)]

        # self.reserve(24)

        def create_vertex(i0, i1, i2, i3, n):
            return [
                self.Vertex(v[i0], n, c[i0], (0, 0)),
                self.Vertex(v[i1], n, c[i1], (0, 0)),
                self.Vertex(v[i2], n, c[i2], (0, 0)),
                self.Vertex(v[i3], n, c[i3], (0, 0))
            ]

        # rear
        self.push_quad(*create_vertex(0, 1, 2, 3, (0, 0, -1)))
        # front
        self.push_quad(*create_vertex(5, 4, 7, 6, (0, 0, 1)))
        # right
        self.push_quad(*create_vertex(1, 5, 6, 2, (1, 0, 0)))
        # left
        self.push_quad(*create_vertex(4, 0, 3, 7, (-1, 0, 0)))
        # bottom
        self.push_quad(*create_vertex(4, 5, 1, 0, (0, -1, 0)))
        # top
        self.push_quad(*create_vertex(6, 7, 3, 2, (0, 1, 0)))

    def calc_normal(self):
        pass
