from level import Level
import math
import random

from kivy.graphics import Scale
from kivy.core.text import Label as CoreLabel

from kivy3 import Material
from kivy3.math.vectors import Vector3

from entities import Entity
from models.shapes import Lines, Quad
from models.portals import PortalPad
from levels.stresstest import StresstestLevel
from levels.level1 import FirstLevel

class Rotor(Entity):
	"""docstring for Rotor"""
	def __init__(self, material, depth, radius, **kwargs):
		super(Rotor, self).__init__(**kwargs)
		self.material = material
		self.depth = depth
		self.radius = radius
		self.rotors = []
		for i in range(3):
			x = math.cos(math.radians(i*120)) * radius
			y = math.sin(math.radians(i*120)) * radius
			self.add(Lines(material, [[0,0,0], [x,0,y]]))
			if depth > 0:
				rotor = Rotor(material, depth-1, radius / 2.)
				rotor.dpos = Vector3([x,0,y])
				self.rotors.append(rotor)
				self.add(rotor)

	def tick(self, df):
		super(Rotor, self).tick(df)
		self.rot.y += df * 3600 * 1/(self.depth*self.depth+1) * (self.depth % 2 -0.5)*2 * math.sin(self.age*0.1)

class TestLevel(Level):
    """docstring for TestLevel"""
    def __init__(self, game):
        super(TestLevel, self).__init__(game)
        self.player.enforce_speed = False

        self.spawn_wireframe_cube([0,-0.5,0], size=[5, 1 ,5])

        self.spawn_portal([0,0,2], color=(0,0,1),
            callback = self.game.load_hub
            )[0].activate()

        self.spawn_text("Fractals\nYay!!!", [0,0,-0.5], size=0.2)

        self.spawn(Rotor(Material(color = (1,1,0)), 3, 1), [0,-0.01,-0.5])
