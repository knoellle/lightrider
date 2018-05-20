#python
import inspect

#kivy
from kivy.core.text import Label as CoreLabel

#kivy3
from kivy3.math.vectors import Vector3
from kivy3.extras.geometries import BoxGeometry
from kivy3 import Material
from kivy3 import PerspectiveCamera
from kivy3 import Scene

#game
from player import Player
from enemies import Stalker
from models.shapes import Cube, Lines, Mesh, Quad
from models.portals import PortalPad
from collider import LineCollider, SphereCollider, BoxCollider

class Level(object):
    def __init__(self, game):
        self.name = ""
        self.game = game
        self.colliders = []
        self.entities = []
        self.time = 0

        # create camera for scene
        self.camera = PerspectiveCamera(
            fov=80,    # distance from the screen
            aspect=0,  # "screen" ratio
            near=.1,    # nearest rendered point
            far=1000     # farthest rendered point
        )
        self.camera.pos.y = 3

        self.scene = Scene()
        self.player = Player()
        self.entities.append(self.player)
        self.scene.add(self.player)

    def tick(self, df):
        self.time += df
        v = self.game.inputVector
        self.player.velocity.add(v * df * 10 * Vector3(-1, 0, 1))
        for e in self.entities:
            e.tick(df)
        self.camera.pos.x = self.player.pos.x+0.3
        self.camera.pos.z = self.player.pos.z-3
        self.camera.look_at(self.player.pos)
        for c in self.colliders:
            if c.callback is not None:
                if c.check(self.player.pos, self.player.size):
                    if len(inspect.getargspec(c.callback)[0]) > 1:
                        if c.callback(c):
                            break
                    else:
                        if c.callback():
                            break
        
    def reset(self):
        for e in self.entities:
            e.reset()

    def spawn(self, entity, position=None):
        if position:
            entity.dpos = Vector3(position)
            entity.reset()

        self.entities.append(entity)
        self.scene.add(entity)
        return entity

    def spawn_text(self, text, position, size=0.1, orientation="y", color=(1,1,1,1)):
        my_label = CoreLabel(font_size=int(200*size))
        my_label.text = text
        my_label.refresh()
        aspect = float(my_label.texture.size[0])/my_label.texture.size[1]

        quad = Quad(Material(map=my_label.texture, color=color[:3], transparency=color[3]), size*aspect, size, orientation=orientation)
        quad.label = my_label
        self.spawn(quad, position)
        
    def spawn_std_cube(self, *args, **kwargs):
        # return self.spawn_wireframe_cube(*args, **kwargs)
        
        return self.spawn_solid_cube(*args, **kwargs)

    def spawn_wireframe_cube(self, location, size=(1,1,1), color=(1,1,1,0.5), callback=None):
        mat = Material(
            color=color[0:3], transparency=color[3]
        )
        cube = Cube(
            material=mat,
            size=size
        )
        cube.dpos = Vector3(location)
        cube.reset()
        self.spawn(cube)
        if callback is not None:
            collider = BoxCollider(p1=p1, p2=p2, parent=cube, callback=callback)
            self.colliders.append(collider)
            return (cube, collider)
        return cube

    def spawn_solid_cube(self, location, texture=None, size=(1,1,1), color=(1,1,1,0.5), callback=None):
        geo = BoxGeometry(size[0], size[1], size[2])
        mat = Material(
            color=color[0:3], transparency=color[3], map=texture
        )
        cube = Mesh(
            geometry=geo,
            material=mat
        )
        self.spawn(cube, location)
        if callback is not None:
            collider = BoxCollider(p1=p1, p2=p2, parent=cube, callback=callback)
            self.colliders.append(collider)
            return (cube, collider)
        return cube

    def spawn_portal(self, position, radius=0.2, color=(1,1,1), callback=None):
        mat = Material(color=color)
        portal = self.spawn(PortalPad(mat, radius, 0.02), position)
        if callback is not None:
            collider = SphereCollider([0,0,0], radius, parent=portal, callback=callback)
            self.colliders.append(collider)
            return (portal, collider)
        return portal

    def spawn_line(self, p1, p2, width=1, color=(1,1,1), callback=None):
        mat = Material(color=color)
        line = Lines(mat, [p1, p2], width)
        self.scene.add(line)
        
        if callback is not None:
            collider = LineCollider(p1=p1, p2=p2, parent=line, callback=callback)
            self.colliders.append(collider)
            return (line, collider)
        return line

    def spawn_stalker(self, position, size=0.1, callback=None):
        stalker = Stalker(level=self)
        stalker.dpos = Vector3(position)
        stalker.reset()
        self.entities.append(stalker)
        self.scene.add(stalker)

        if callback is not None:
            collider = SphereCollider(position=(0,0,0),radius=size, parent=stalker, callback=callback)
            self.colliders.append(collider)
            return (stalker, collider)
        return stalker