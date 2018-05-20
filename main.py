# coding: utf-8

# fullscreen setup
from kivy.config import Config
# Config.set('graphics', 'fullscreen', 'auto')

# python
from random import random
from os.path import join, dirname, abspath
import math

# kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup

# kivy3
from kivy3 import Renderer, Scene
from kivy3.loaders import OBJLoader
from kivy3.core.object3d import Object3D
from kivy3.extras.geometries import BoxGeometry
from kivy3 import Material, Mesh
from kivy3.math.vectors import Vector3
from kivy.graphics import Color, Line

# game
from player import Player
from levels.hub import HubLevel
from levels.stresstest import StresstestLevel
from models.shapes import Ellipse
from circle import Circle

Builder.load_string('''
<LightPanel@BoxLayout>:
    Widget:
''')

FOLDER = dirname(abspath(__file__))

class Joystick(Widget):
    def __init__(self, **kwargs):
        super(Joystick, self).__init__(**kwargs)
        self.vector = Vector3(0,0,0)
        self.opacity = 0
        with self.canvas:
            self.base = Line(circle=(75,75,60))
            self.stick = Line(circle=(75,75,75))

    def update(self, v1, v2):
        self.base.circle = (v1.x, v1.z, 60)
        self.stick.circle = (v1.x+v2.x*60, v1.z+v2.z*60, 75)

class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)

        self.renderer = None
        self.load_hub()
        self.bind(size=self.resizeRenderer)

        Clock.schedule_interval(self.game_loop, 1.0/60)

        self.joystick = Joystick()
        self.add_widget(self.joystick, index=0)

    def load_hub(self):
        self.load_level(HubLevel(self))

    def load_level(self, level):
        self.level = level
        self.inputVector = Vector3([0,0,0])

        # (re)create renderer
        if self.renderer:
            self.remove_widget(self.renderer)
        self.renderer = Renderer(size_hint=(5, 5),shader_file="flat.glsl")
        self.add_widget(self.renderer, index=1)
        self.renderer.set_clear_color(
            (0, 0, 0, 1)
        )  # rgba

        # e.g. when added to parent
        self.renderer.bind(size=self._adjust_aspect)

        self.renderer.render(level.scene, level.camera)
        self.resizeRenderer()

    def _adjust_aspect(self, *args):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def resizeRenderer(self, *args):
        self.renderer.size = self.size

    def game_loop(self, *df):
        print("FPS: {:.2f}".format(1/df[0]))
        self.level.tick(df[0])

    def on_touch_down(self, touch):
        self.touchStart = Vector3([touch.x, 0, touch.y])
        self.inputVector = Vector3([0,0,0])
        self.update_joystick()
        self.joystick.opacity = 1

    def on_touch_move(self, touch):
        v = Vector3([touch.x, 0, touch.y]) - self.touchStart
        l = v.length()
        if l > 0:
            v = v * (1/v.length())

        v = v * (min(60,l) / 60)
        self.inputVector = v
        self.update_joystick()

    def on_touch_up(self, touch):
        self.inputVector = Vector3([0,0,0])
        self.joystick.opacity = 0

    def update_joystick(self):
        self.joystick.update(self.touchStart, self.inputVector)

class My3D(App):
    def build(self):
        self.game = Game()
        return self.game
My3D().run()