#kivy3
from kivy3 import Material
from kivy3.math.vectors import Vector3

#game
from entities import Entity
from models.shapes import Ellipse

class Player(Entity):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        mat = Material(
            color=(1, 0, 0), transparency=1
        )
        self.speed = 1
        self.enforce_speed = True
        self.acceleration = 1
        self.size = 0.1
        self.model = Ellipse(mat, self.size, 36)
        self.add(self.model)

    def add_to_scene(self, scene):
        super(Player, self).add_to_scene(scene)

    def tick(self, df):
        super(Player, self).tick(df)

        target = Vector3([0,0,0])
        l = self.velocity.length()
        if self.enforce_speed and l>0:
            target = self.velocity * (1/l)

        self.velocity = self.velocity + (target - self.velocity) * min(self.acceleration * df, 1.)
        print(self.velocity.length(), self.velocity)
        if self.velocity.length() > self.speed:
            self.velocity = self.velocity.normalize()
        print(self.velocity.length(), self.velocity)
