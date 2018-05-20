"""
The MIT License (MIT)

Copyright (c) 2013 Niko Skrypnik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from kivy.graphics import Mesh as KivyMesh
from kivy3 import Vector3
from kivy3.core.object3d import Object3D
import math

DEFAULT_VERTEX_FORMAT = [
    (b'v_pos', 3, 'float'),
    (b'v_normal', 3, 'float'),
    (b'v_tc0', 2, 'float')]


class Circle(Object3D):

    def __init__(self, radius, num_points, color=(1,1,1,1), **kw):
        super(Object3D, self).__init__(**kw)
        self.radius = radius
        self.num_points = num_points
        self.color = color
        self.vertex_format = kw.pop("vertex_format", DEFAULT_VERTEX_FORMAT)
        self.create_mesh()

    def create_mesh(self):
        """ Create real mesh object from the geometry and material """
        vertices = [Vector3([0,0,0])]
        indices = [0]
        a = math.radians(360 / self.num_points)
        for i in range(self.num_points):
            vertices.append(Vector3([math.cos(a*i)*self.radius,
                                    0,
                                    math.sin(a*i)*self.radius]))
            indices.append(len(indices))
        kw = {"vertices": vertices, "indices": indices,
              "fmt": self.vertex_format, "mode": "triangle_fan"
              }
        # if self.material.map:
        #     kw["texture"] = self.material.map
        self._mesh = KivyMesh(**kw)

    def material(self):
      pass

    def custom_instructions(self):
        yield self.material
        yield self._mesh
