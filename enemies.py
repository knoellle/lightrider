from kivy3 import Material, Mesh

#game
from entities import Entity
from models.shapes import Star

class Stalker(Entity):
    def __init__(self, **kwargs):
        super(Stalker, self).__init__(**kwargs)
        mat = Material(color=(1,0,0))
        self.add(Star(mat, 0.03, 0.1, 10))
        
    def tick(self, df):
        super(Stalker, self).tick(df)
        self.rot.y += self.velocity.length() * 120 * df
        self.velocity = self.velocity * (1 - df)
        if self.velocity.length() < 1:
            self.velocity = self.velocity + (self.level.player.position - self.position).normalize() * 3