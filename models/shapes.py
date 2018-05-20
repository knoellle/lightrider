import math

from kivy.graphics import Mesh as KivyMesh
from kivy.graphics import Callback, Point
from kivy.graphics.opengl import glLineWidth

from kivy3 import Vector3
from entities import Entity

DEFAULT_VERTEX_FORMAT = [
    (b'v_pos', 3, 'float')
    ,(b'v_normal', 3, 'float')
    ,(b'v_tc0', 2, 'float')
    ]

class Cube(Entity):

    def __init__(self, material, size=(1,1,1), **kw):
        super(Cube, self).__init__(**kw)
        self.material = material
        self.vertex_format = kw.pop("vertex_format", DEFAULT_VERTEX_FORMAT)
        self.mode = kw.pop("mode", "lines")
        self.size = Vector3(size)
        self.create_mesh()

    def create_mesh(self):
        """ Create real mesh object from the geometry and material """
        x,y,z = 0.5*self.size.x, 0.5*self.size.y, 0.5*self.size.z
        vertices = [ x, y, z,  x, y, z,  0, 0,
                    -x, y, z, -x, y, z,  0, 0,
                    -x, y,-z, -x, y,-z,  0, 0,
                     x, y,-z,  x, y,-z,  0, 0,
                     x,-y, z,  x,-y, z,  0, 0,
                    -x,-y, z, -x,-y, z,  0, 0,
                    -x,-y,-z, -x,-y,-z,  0, 0,
                     x,-y,-z,  x,-y,-z,  0, 0]
        indices = [0,1, 1,2, 2,3, 3,0,
                   4,5, 5,6, 6,7, 7,4,
                   0,4, 1,5, 2,6, 3,7]

        kw = {"vertices": vertices, "indices": indices,
              "fmt": self.vertex_format, "mode": self.mode
              }
        if self.material.map:
            kw["texture"] = self.material.map
        self._mesh = KivyMesh(**kw)

    def custom_instructions(self):
        yield self.material
        yield self._mesh

DEFAULT_VERTEX_FORMAT = [
    (b'v_pos', 3, 'float'),
    (b'v_normal', 3, 'float'),
    (b'v_tc0', 2, 'float')]

class Mesh(Entity):

    def __init__(self, geometry, material, **kw):
        super(Mesh, self).__init__(**kw)
        self.geometry = geometry
        self.material = material
        self.mtl = self.material  # shortcut for material property
        self.vertex_format = kw.pop("vertex_format", DEFAULT_VERTEX_FORMAT)
        self.mode = kw.pop("mode", "triangle")
        self.create_mesh()

    def create_mesh(self):
        """ Create real mesh object from the geometry and material """
        vertices = []
        indices = []
        idx = 0
        for face in self.geometry.faces:
            for i, k in enumerate(['a', 'b', 'c']):
                v_idx = getattr(face, k)
                vertex = self.geometry.vertices[v_idx]
                vertices.extend(vertex)
                try:
                    normal = face.vertex_normals[i]
                except IndexError:
                    normal = Vector3([0, 0, 0])
                vertices.extend(normal)
                try:
                    tex_coords = self.geometry.face_vertex_uvs[0][idx]
                    vertices.extend(tex_coords)
                except IndexError:
                    vertices.extend([0, 0])
                indices.append(idx)
                idx += 1
        kw = {"vertices": vertices, "indices": indices,
              "fmt": self.vertex_format, "mode": self.mode
              }
        if self.material.map:
            kw["texture"] = self.material.map
        self._mesh = KivyMesh(**kw)

    def custom_instructions(self):
        super(Mesh, self).custom_instructions()
        yield self.material
        yield self._mesh

class Lines(Entity):
  """docstring for Lines"""
  def __init__(self, material, points, width=1, **kw):
    super(Lines, self).__init__(**kw)
    self.material = material
    self.points = points
    self.width = width
    self.vertex_format = kw.pop("vertex_format", DEFAULT_VERTEX_FORMAT)
    self.mode = kw.pop("mode", "lines")
    self.create_mesh()

  def create_mesh(self):
    """ Create real mesh object from the geometry and material """
    vertices = []
    indices = []

    for p in self.points:
      vertices.extend(list(p) + [0,1,0,  p[0], p[2]])
      indices.append(len(indices))

    kw = {"vertices": vertices, "indices": indices,
          "fmt": self.vertex_format, "mode": self.mode
          }
    if self.material.map:
        kw["texture"] = self.material.map
    self._mesh = KivyMesh(**kw)

  def prepare(self, *args):
    glLineWidth(self.width)

  def cleanup(self, *args):
    glLineWidth(1)

  def custom_instructions(self):
    yield Callback(self.prepare)
    yield self.material
    yield self._mesh
    yield Callback(self.cleanup)

class Ellipse(Entity):

    def __init__(self, material, radius, segments, **kw):
        super(Ellipse, self).__init__(**kw)
        self.material = material
        self.radius = radius
        self.segments = segments
        self.vertex_format = kw.pop("vertex_format", DEFAULT_VERTEX_FORMAT)
        self.mode = kw.pop("mode", "triangle_fan")
        self.create_mesh()

    def create_mesh(self):
        """ Create real mesh object from the geometry and material """
        vertices = []
        indices = []

        a = math.radians(360 / self.segments)
        for i in range(self.segments):
            tx = math.cos(i * a); x = tx * self.radius
            y = 0
            tz = math.sin(i * a); z = tz * self.radius
            vertices.extend([x,y,z,  0,1,0,  tx*0.5+0.5,tz*0.5+0.5])
            indices.append(len(indices))

        kw = {"vertices": vertices, "indices": indices,
            "fmt": self.vertex_format, "mode": self.mode
            }
        if self.material.map:
          kw["texture"] = self.material.map
        self._mesh = KivyMesh(**kw)

    def custom_instructions(self):
        yield self.material
        yield self._mesh

class Quad(Entity):
    """docstring for Quad"""
    def __init__(self, material, width, height, orientation = "y", **kw):
        super(Quad, self).__init__(**kw)
        self.material = material
        self.width = width
        self.height = height
        self.orientation = orientation
        self.vertex_format = kw.pop("vertex_format", DEFAULT_VERTEX_FORMAT)
        self.mode = kw.pop("mode", "triangle_fan")
        self.create_mesh()

    def create_mesh(self):
        """ Create real mesh object from the geometry and material """
        vertices = []
        indices = [0,1,2,3]

        # define basis vectors
        if self.orientation == "x":
            bx = Vector3([0,0,-1])
            by = Vector3([0,-1,0])
            normal = Vector3([-1,0,0])
        elif self.orientation == "y":
            bx = Vector3([-1,0,0])
            by = Vector3([0,0,-1])
            normal = Vector3([0,1,0])
        else:
            bx = Vector3([-1,0,0])
            by = Vector3([0,-1,0])
            normal = Vector3([0,0,1])

        bx = bx * 0.5 * self.width
        by = by * 0.5 * self.height

        vertices.extend(list(bx*-1 + by*-1) + list(normal) + [0,0])
        vertices.extend(list(bx* 1 + by*-1) + list(normal) + [1,0])
        vertices.extend(list(bx* 1 + by* 1) + list(normal) + [1,1])
        vertices.extend(list(bx*-1 + by* 1) + list(normal) + [0,1])

        kw = {"vertices": vertices, "indices": indices,
            "fmt": self.vertex_format, "mode": self.mode
            }
        if self.material.map:
          kw["texture"] = self.material.map
        self._mesh = KivyMesh(**kw)

    def custom_instructions(self):
        yield self.material
        yield self._mesh

class Star(Entity):
  """docstring for Star"""
  def __init__(self, material, inner_radius, outer_radius, peaks=5, width=1, **kw):
    super(Star, self).__init__(**kw)
    self.material = material
    self.inner_radius = inner_radius
    self.outer_radius = outer_radius
    self.peaks = peaks
    self.width = width
    self.vertex_format = kw.pop("vertex_format", DEFAULT_VERTEX_FORMAT)
    self.mode = kw.pop("mode", "line_loop")
    self.create_mesh()

  def create_mesh(self):
    """ Create real mesh object from the geometry and material """
    vertices = []
    indices = []

    a = math.radians(360 / (self.peaks*2))
    for i in range(int(self.peaks*2)):
      tx = math.cos(i * a); x = tx * (self.inner_radius + (i % 2) * (self.outer_radius-self.inner_radius))
      y = 0
      tz = math.sin(i * a); z = tz * (self.inner_radius + (i % 2) * (self.outer_radius-self.inner_radius))
      vertices.extend([x,y,z,  0,1,0,  x,z])
      indices.append(len(indices))

    kw = {"vertices": vertices, "indices": indices,
          "fmt": self.vertex_format, "mode": self.mode
          }
    if self.material.map:
        kw["texture"] = self.material.map
    self._mesh = KivyMesh(**kw)

  def prepare(self, *args):
    glLineWidth(self.width)

  def cleanup(self, *args):
    glLineWidth(1)

  def custom_instructions(self):
    yield Callback(self.prepare)
    yield self.material
    yield self._mesh
    yield Callback(self.cleanup)
