from level import Level
import math
import random

from kivy.graphics import Scale

from kivy3 import Material
from kivy3.math.vectors import Vector3

from models.shapes import Lines, Ellipse, Quad
from models.portals import PortalPad
from levels.stresstest import StresstestLevel
from levels.test import TestLevel
from levels.level1 import FirstLevel

class HubLevel(Level):
    def __init__(self, game):
        super(HubLevel, self).__init__(game)

        # debug and testing
        self.spawn_text("Testlevels", [1,-0.1,-1])
        self.spawn_text("Stresstest", [0,-0.1,-0.5], size=0.1)
        self.spawn_portal([0,0,-1], color=(0,0,1),
            callback = lambda: self.game.load_level(StresstestLevel(self.game))
            )[0].activate()
        self.spawn_text("Misc. Test", [-1,-0.1,-0.5], size=0.1)
        self.spawn_portal([-1,0,-1], color=(0,0,1),
            callback = lambda: self.game.load_level(TestLevel(self.game))
            )[0].activate()

        #actual levels
        self.spawn_text("Levels", [1,-0.1,1])
        self.spawn_text("1", [0,-0.1,0.5], size=0.3)
        self.spawn_portal([0,0,1], color=(0,1,0),
            callback=lambda: self.game.load_level(FirstLevel(self.game)) 
            )[0].activate()

        #frame
        self.spawn(Quad(Material(transparency=0.5), 3, 3, mode="line_loop"))
        self.spawn(Quad(Material(transparency=0.5), 3.1, 3.1, mode="line_loop"),[0,-0.05,0])

    def tick(self, df):
        super(HubLevel, self).tick(df)

    def load_stresstest(self):
        self.game.load_level(StresstestLevel(self.game))
        return True

    def load_level1(self):
        self.game.load_level(FirstLevel(self.game))
        return True