import random
import math

from kivy.graphics import Scale

from kivy3 import Material
from kivy3.math.vectors import Vector3

from models.shapes import Lines, Ellipse, Cube, Star
from level import Level
from enemies import Stalker
from entities import Entity
from collider import LineCollider, SphereCollider
from models.portals import PortalPad

class Lift(Entity):
    def __init__(self, **kwargs):
        super(Lift, self).__init__(**kwargs)
        self.state = 0
        self.mat1 = Material(color=(1,1,1),transparency=0.5)
        self.mat2 = Material(color=(1,1,0))
        self.add(Cube(self.mat1, level=self.level))
        self.add(Lines(self.mat2, [(0,0,0), (0,15,0)], level=self.level))
        self.circle = Star(self.mat2, 0.3, 0.3, 36)
        self.circle.set_pos([0,0.5,0])
        self.add(self.circle)
        self.level.colliders.append(LineCollider((0,0,0),(0,15,0),parent=self,callback=self.activate))

    def reset(self):
        super(Lift, self).reset()
        self.state = 0
        self.velocity.y = 0
        self.mat1.transparency = 0.5
        self.mat2.color = (1.,1.,0.)

    def activate(self):
        if self.state == 1:
            return
        self.level.liftcount = self.level.liftcount-1
        self.state = 1
        self.mat1.transparency = 1
        self.mat2.color = (1.,1.,1.)

    def tick(self, df):
        super(Lift, self).tick(df)
        self.circle.scale.xyz = (math.sin(self.age), math.sin(self.age), math.sin(self.age))
        if self.state == 1:
            if self.velocity.y < 1:
                self.velocity.y += df

class FirstLevel(Level):
    def __init__(self, game):
        super(FirstLevel, self).__init__(game)
        self.liftcount = 9
        for x in range(3):
            for z in range(3):
                cx = (x-1)*2
                cz = (z-1)*2
                self.spawn(Lift(level=self), (cx, -.55, cz))
        
        mat = Material(color=(0,1,0))

        self.portal = self.spawn(PortalPad(mat, 0.2, 0.02), [0 ,0, 0])
        self.colliders.append(SphereCollider([0,0,0], self.portal.radius, parent=self.portal, callback=self.load_hub))
        self.spawn_line([1,0,1], [-1,0,1], color=(1,0,0), callback=self.reset)
        self.spawn_line([-1,0,-1], [-1,0,1], color=(1,0,0), callback=self.reset)
        self.spawn_line([1,0,-1], [1,0,1], color=(1,0,0), callback=self.reset)

    def reset(self):
        super(FirstLevel, self).reset()
        self.liftcount = 9
        # self.

    def tick(self, df):
        super(FirstLevel, self).tick(df)
        if self.liftcount == 0:
            self.portal.activate()

    def load_hub(self):
        if self.portal.step >= 1.:
            self.game.load_hub()
            return True
        return False