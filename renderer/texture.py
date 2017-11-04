# pylint: disable=W0401,W0614,W0621,W0622
from logging import getLogger
logger = getLogger(__name__)

from OpenGL.GL import *


class Texture:
    def __init__(self):
        self.texture = None
        self.sampler = None
        self.image = None

    def create_texture(self, w, h, data):
        size = len(data)
        assert size == w * h * 4
        self.image = (w, h, data)

    def initialize(self):
        self.sampler = glGenSamplers(1)
        glSamplerParameteri(self.sampler, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glSamplerParameteri(self.sampler, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glSamplerParameteri(self.sampler, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glSamplerParameteri(self.sampler, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        if self.image:
            #logger.info('initialize texture')
            w, h, data = self.image
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0,
                         GL_RGBA, GL_UNSIGNED_BYTE, data)
        else:
            #logger.info('initialize texture. default white')
            # white
            w = 4
            h = 4
            data = [255 for x in range(w * h * 4)]
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0,
                         GL_RGBA, GL_UNSIGNED_BYTE, data)

    def bind(self):
        if not self.texture:
            self.initialize()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBindSampler(0, self.sampler)
