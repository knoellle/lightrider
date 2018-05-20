import math
import random

from kivy.graphics import Scale

from kivy3 import Material
from kivy3.math.vectors import Vector3

import collider
from level import Level
from models.portals import PortalPad
from models.shapes import Lines, Ellipse
from collider import LineCollider, SphereCollider

class StresstestLevel(Level):
    def __init__(self, game):
        super(StresstestLevel, self).__init__(game)
        points = []
        for i in range(12*4000):
            points.append([math.cos(i*2)*i/24000,
                           math.sqrt(math.sqrt(math.sqrt(i/24000.))),
                           math.sin(i*2)*i/24000])
        mat = Material(color=(1,1,1))
        self.lines = Lines(mat, points)
        self.lines.set_pos([0,-1,0])
        self.scene.add(self.lines)

        mat = Material(color=(0,1,0))
        self.portal = self.spawn(PortalPad(mat, 0.2, 0.02), [0 ,0, 3])
        self.portal.activate()
        self.colliders.append(SphereCollider([0,0,0], self.portal.radius, parent=self.portal, callback=self.load_hub))

    def tick(self, df):
        super(StresstestLevel, self).tick(df)
        self.lines.rot.y += df * 120

    def load_hub(self):
        if self.portal.step >= 1.:
            self.game.load_hub()
            return True
        return False