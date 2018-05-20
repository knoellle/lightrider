#kivy3
from kivy3 import Material

#game
from entities import Entity
from models.shapes import Ellipse

class Player(Entity):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        mat = Material(
            color=(1, 0, 0), transparency=1
        )
        self.size = 0.1
        self.model = Ellipse(mat, self.size, 36)
        self.add(self.model)

    def add_to_scene(self, scene):
        super(Player, self).add_to_scene(scene)

    def tick(self, df):
        super(Player, self).tick(df)