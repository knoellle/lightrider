import math

from kivy.graphics import Mesh as KivyMesh
from kivy.graphics import Callback
from kivy.graphics.opengl import glLineWidth

from kivy3 import Vector3
from entities import Entity
from models.shapes import Star

class PortalPad(Entity):
    def __init__(self, material, radius=0.2, height=0.02, width=1, **kw):
        super(PortalPad, self).__init__(**kw)
        self.material = material
        self.radius = radius
        self.height = height
        self.width = width
        self.step = 0
        self.active = False
        self.animation_speed = 0.25
        self.rings = [Star(material, radius, radius, 36, width),
                      Star(material, radius, radius, 36, width),
                      Star(material, radius, radius, 36, width)]
        self.generator = [Star(material, radius, radius, 1.5, width),
                          Star(material, radius, radius, 1.5, width)]
        for r in self.rings + self.generator:
            self.add(r)

    def reset(self):
        super(PortalPad, self).reset()
        self.step = 0
        self.active = False

    def activate(self):
        if not self.active:
            self.step = 0            
        self.active = True

    def animate(self, f = None):
        self.step = f
        if f <= 0:
            for i,r in enumerate(self.rings+self.generator):
                r.set_pos([0,100,0])
            return
        self.material.transparency = 0.5
        if f >= 1:
            self.material.transparency = 1.
        for i,r in enumerate(self.rings+self.generator):
            if f < 0.5:
                r.set_pos([0,0,0])
                r.scale.xyz = (f*2, 1, f*2)
            elif f < 1:
                r.set_pos([0, i*(f-0.5)*self.height, 0])
                r.scale.xyz = (1-(f-0.5)*0.2*i, 1, 1-(f-0.5)*0.2*i)

    def tick(self, df):
        super(PortalPad, self).tick(df)
        if self.active:
            self.step = min(self.step + df * self.animation_speed, 1)
        self.animate(self.step)
        self.generator[0].rot.y += self.step * df * +1800
        self.generator[1].rot.y += self.step * df * -1800
