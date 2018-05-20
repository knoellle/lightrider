#kivy3
from kivy3.core.object3d import Object3D
from kivy3.math.vectors import Vector3

class Entity(Object3D):
    def __init__(self, level=None, **kwargs):
        super(Entity, self).__init__(**kwargs)
        self.level = level
        self.age = 0
        self.velocity = Vector3([0, 0, 0])
        self.dpos = Vector3([0,0,0])
        self.dvel = Vector3([0,0,0])

    def tick(self, df):
        self.age += df
        # self.position.add(self.velocity * df)
        self.position.x += self.velocity.x * df
        self.position.y += self.velocity.y * df
        self.position.z += self.velocity.z * df
        for c in self.children:
            if isinstance(c, Entity):
                c.tick(df)

    def add_to_scene(self, scene):
        scene.add(self)

    def set_pos(self, v):
        self.position.x = v[0]
        self.position.y = v[1]
        self.position.z = v[2]

    def reset(self):
        self.age = 0
        self.set_pos(self.dpos)
        self.velocity = self.dvel
        for c in self.children:
            if isinstance(c, Entity):
                c.reset()