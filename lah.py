'''
Linear Algebra Helper

This library is row vector style and matrix use row major layout.
(DirectX style)

# mult order

pos = vec4 * Model * View * Projection
    = vec4 * MVP

# row major layout

| 0  1  2  3|
| 4  5  6  7|
| 8  9 10 11|
|12 13 14 15|

# glsl(col major) 

glUniformMatrix4fv(loc, cnt, False, matrix)
(transposed)

## col major layout

| 0  4  8 12|
| 1  5  9 13|
| 2  6 10 14|
| 3  7 11 15|

GL_Position = PVM * vPosition;

# glsl(row major)

glUniformMatrix4fv(loc, cnt, True, matrix)
(not transposed)

GL_Position = vPosition * MVP;
'''

import math


TO_RADIANS = math.pi / 180


class Vec3:
    def __init__(self, *args):
        if len(args) != 3:
            raise ValueError('Vec3.__init__')
        self.array = [args[0], args[1], args[2]]

    def __repr__(self)->str:
        return f'[{self.x}, {self.y}, {self.z}]'

    @property
    def x(self): return self.array[0]

    @property
    def y(self): return self.array[1]

    @property
    def z(self): return self.array[2]

    @staticmethod
    def zero():
        return Vec3(0, 0, 0)

    def __sub__(self, rhs):
        return Vec3(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)

    def __mul__(self, factor):
        return Vec3(self.x * factor, self.y * factor, self.z * factor)

    def dot(self, rhs):
        return self.x * rhs.x + self.y * rhs.y + self.z * rhs.z

    def cross(self, rhs):
        return Vec3(self.y * rhs.z - self.z * rhs.y,
                    self.z * rhs.x - self.x * rhs.z,
                    self.x * rhs.y - self.y * rhs.x)

    def __iter__(self):
        return self.array.__iter__()

    @property
    def sqnorm(self): return self.dot(self)

    @property
    def norm(self): return math.sqrt(self.sqnorm)

    @property
    def normalized(self): return self * (1 / self.norm)


class Vec4:
    def __init__(self, *args):
        if isinstance(args[0], Vec3):
            self.array = [args[0].x, args[0].y, args[0].z, args[1]]
        else:
            if len(args) != 4:
                raise ValueError('Vec4.__init__')
            self.array = [args[0], args[1], args[2], args[3]]

    @property
    def x(self): return self.array[0]

    @property
    def y(self): return self.array[1]

    @property
    def z(self): return self.array[2]

    @property
    def w(self): return self.array[3]

    def __iter__(self):
        return self.array.__iter__()

    @property
    def vec3(self):
        return Vec3(self.x, self.y, self.z)

    @property
    def vec3_w_normalized(self):
        return Vec3(self.x / self.w, self.y / self.w, self.z / self.w)

    def dot(self, rhs):
        return (self.x * rhs.x +
                self.y * rhs.y +
                self.z * rhs.z +
                self.w * rhs.w)


class Quaternion:
    def __init__(self, x, y, z, w):
        self.array = [x, y, z, w]

    def __repr__(self)->str:
        return f'[{self.x}, {self.y}, {self.z}, {self.w}]'

    @property
    def x(self): return self.array[0]

    @property
    def y(self): return self.array[1]

    @property
    def z(self): return self.array[2]

    @property
    def w(self): return self.array[3]

    def axis_angle(self):
        angle = 2 * math.acos(self.w)
        s = math.sqrt(1 - self.w * self.w)
        if (s < 0.001):
            x = self.x
            y = self.y
            z = self.z
        else:
            x = self.x / s
            y = self.y / s
            z = self.z / s
        return Vec3(x, y, z), angle

    @staticmethod
    def identity():
        return Quaternion(0, 0, 0, 1)

    @staticmethod
    def from_axis_angle(axis, angle):
        s = math.sin(angle / 2)
        x = axis.x * s
        y = axis.y * s
        z = axis.z * s
        w = math.cos(angle / 2)
        return Quaternion(x, y, z, w)

    @property
    def mat3(self):
        return Mat3(1 - 2 * self.y * self.y - 2 * self.z * self.z,
                    2 * self.x * self.y + 2 * self.w * self.z,
                    2 * self.x * self.z - 2 * self.w * self.y,

                    2 * self.x * self.y - 2 * self.w * self.z,
                    1 - 2 * self.x * self.x - 2 * self.z * self.z,
                    2 * self.y * self.z + 2 * self.w * self.x,

                    2 * self.x * self.z + 2 * self.w * self.y,
                    2 * self.y * self.z - 2 * self.w * self.x,
                    1 - 2 * self.x * self.x - 2 * self.y * self.y
                    )


class Mat3:
    def __init__(self, *args):
        if isinstance(args[0], Vec3):
            if len(args) != 3:
                raise ValueError('Mat3.__init__ 3')
            self.array = [args[0].x, args[0].y, args[0].z,
                          args[1].x, args[1].y, args[1].z,
                          args[2].x, args[2].y, args[2].z,
                          ]
        else:
            if len(args) != 9:
                raise ValueError('Mat3.__init__ 9')
            self.array = [args[0], args[1], args[2],
                          args[3], args[4], args[5],
                          args[6], args[7], args[8]]

    def row(self, n):
        return Vec3(*self.array[n * 3:n * 3 + 3])

    def col(self, n):
        return Vec3(*self.array[n:9:3])


class Mat4:
    def __init__(self, *args):
        if isinstance(args[0], Vec4):
            if len(args) != 4:
                raise ValueError('Mat4.__init__ 4')
            self.array = [args[0].x, args[0].y, args[0].z, args[0].w,
                          args[1].x, args[1].y, args[1].z, args[1].w,
                          args[2].x, args[2].y, args[2].z, args[2].w,
                          args[3].x, args[3].y, args[3].z, args[3].w
                          ]
        else:
            if len(args) != 16:
                raise ValueError('Mat4.__init__ 16')
            self.array = [args[0], args[1], args[2], args[3],
                          args[4], args[5], args[6], args[7],
                          args[8], args[9], args[10], args[11],
                          args[12], args[13], args[14], args[15]]

    def row(self, n):
        return Vec4(*self.array[n * 4:n * 4 + 4])

    def col(self, n):
        return Vec4(*self.array[n:16:4])

    @property
    def lefttop3(self):
        return Mat3(self.row(0).vec3, self.row(1).vec3, self.row(2))

    @property
    def transposed(self):
        return Mat4(self.col(0), self.col(1), self.col(2), self.col(3))

    '''
    def __eq__(self, rhs):
        for i in range(16):
            if(math.abs(self.array[i] - rhs.array[i]) > 1e-4):
                return False
        return True
    '''

    def __mul__(self, rhs):
        return Mat4(
            self.row(0).dot(rhs.col(0)),
            self.row(0).dot(rhs.col(1)),
            self.row(0).dot(rhs.col(2)),
            self.row(0).dot(rhs.col(3)),
            self.row(1).dot(rhs.col(0)),
            self.row(1).dot(rhs.col(1)),
            self.row(1).dot(rhs.col(2)),
            self.row(1).dot(rhs.col(3)),
            self.row(2).dot(rhs.col(0)),
            self.row(2).dot(rhs.col(1)),
            self.row(2).dot(rhs.col(2)),
            self.row(2).dot(rhs.col(3)),
            self.row(3).dot(rhs.col(0)),
            self.row(3).dot(rhs.col(1)),
            self.row(3).dot(rhs.col(2)),
            self.row(3).dot(rhs.col(3))
        )

    def apply(self, v):
        if isinstance(v, Vec3):
            v4 = Vec4(v, 1)
        elif isinstance(v, Vec4):
            v4 = v
        else:
            raise ValueError('apply')

        applied = Vec4(v4.dot(self.col(0)),
                       v4.dot(self.col(1)),
                       v4.dot(self.col(2)),
                       v4.dot(self.col(3))
                       )

        if isinstance(v, Vec3):
            return applied.vec3
        else:
            return applied

    @staticmethod
    def identity():
        return Mat4(1, 0, 0, 0,
                    0, 1, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 0, 1
                    )

    @staticmethod
    def orthognonal(l, r, b, t, n, f):
        return Mat4(
            2 / (r - l), 0, 0, 0,
            0, 2 / (t - b), 0, 0,
            0, 0, 2 / (f - n), 0,
            -(r + l) / (r - l), -(t + b) / (t - b), -(n + f) / (f - n), 1
        )

    @staticmethod
    def pinhole(fovy, aspect, n, f):
        tan = math.atan(fovy * TO_RADIANS / 2)
        f = 1 / tan
        return Mat4(f / aspect, 0, 0, 0,
                    0, f, 0, 0,
                    0, 0, 2 / (f - n), 1,
                    0, 0, -(n + f) / (f - n), 0
                    )

    @staticmethod
    def perspective_rh(fovy, aspect, zNear, zFar):
        tan = math.atan(fovy * TO_RADIANS / 2)
        f = 1 / tan
        return Mat4(f / aspect, 0, 0, 0,
                    0, f, 0, 0,
                    0, 0, (zFar + zNear) / (zNear - zFar), -1,
                    0, 0, 2 * zFar * zNear / (zNear - zFar), 0
                    )

    @staticmethod
    def perspective_lh(fovy, aspect, zNear, zFar):
        tan = math.atan(fovy * TO_RADIANS / 2)
        f = 1 / tan
        return Mat4(f / aspect, 0, 0, 0,
                    0, f, 0, 0,
                    0, 0, (zFar + zNear) / (zFar - zNear), -1,
                    0, 0, 2 * zFar * zNear / (zFar - zNear), 0
                    )

    @staticmethod
    def translate(x, y, z):
        return Mat4(1, 0, 0, 0,
                    0, 1, 0, 0,
                    0, 0, 1, 0,
                    x, y, z, 1
                    )

    @staticmethod
    def rotateXAxisByDegrees(degree):
        rad = degree * TO_RADIANS
        s = math.sin(rad)
        c = math.cos(rad)
        return Mat4(1, 0, 0, 0,
                    0, c, s, 0,
                    0, -s, c, 0,
                    0, 0, 0, 1
                    )

    @staticmethod
    def rotateYAxisByDegrees(degree):
        rad = degree * TO_RADIANS
        s = math.sin(rad)
        c = math.cos(rad)
        return Mat4(c, 0, -s, 0,
                    0, 1, 0, 0,
                    s, 0, c, 0,
                    0, 0, 0, 1
                    )

    @staticmethod
    def rotateZAxisByRadians(rad):
        s = math.sin(rad)
        c = math.cos(rad)
        return Mat4(c, s, 0, 0,
                    -s, c, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 0, 1
                    )


class Transform:
    def __init__(self, pos, rot):
        self.pos = pos
        self.rot = rot

    @staticmethod
    def identity():
        return Transform(Vec3.zero(), Quaternion.identity())

    @property
    def mat4(self):
        r = self.rot.mat3
        return Mat4(
            Vec4(r.row(0), 0),
            Vec4(r.row(1), 0),
            Vec4(r.row(2), 0),
            Vec4(self.pos, 1)
        )
