from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from lib.pvector import PVector
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from plyer import accelerometer
import numpy as np
from random import randint

import math
from room import Room


class Ball(Widget):
    vel = PVector(0, 0)
    acc = PVector(0, 0)
    mass = 50

    def move(self):
        self.vel += self.acc
        # self.vel.limit(10)
        self.pos = PVector(self.pos) + self.vel
        self.acc *= 0

    def checkEdge(self):
        if self.center[0] > Window.width:
            self.center[0] = Window.width
            self.vel[0] *= -1

        elif self.center[0] < 0:
            self.vel[0] *= -1
            self.center[0] = 0

        if self.center[1] > Window.height:
            self.center[1] = Window.height
            self.vel[1] *= -1
        elif self.center[1] < 100:
            self.center[1] = 100
            self.vel[1] *= -1

    def applyForce(self, force):
        acc = force / self.mass
        self.acc += acc


class Level(BoxLayout):
    ball = ObjectProperty()
    acc_label = ObjectProperty()
    fri_label = ObjectProperty()
    button = ObjectProperty()
    room = ObjectProperty()

    def __init__(self, *args):
        super(Level, self).__init__(*args)
        self.sensorEnabled = False
        self.fric_coef = .05
        self.grav = PVector(0, 0)
        self.room.center = randint(0, Window.width), randint(0, Window.height)
        self.ball.center = self.room.center
        self.room.init_room()


    def get_mouse_gravity(self):
        # Compute gravity
        gravity = PVector(Window.mouse_pos) - PVector(self.center)
        gravity.x = float(np.interp(gravity[0], [-400, 400], [-10, 10]))
        gravity.y = float(np.interp(gravity[1], [-300, 300], [-10, 10]))
        return gravity

    def get_friction(self):
        angle_in_rad = PVector.acc_to_rad(self, self.grav)
        return - angle_in_rad * self.ball.mass * self.ball.vel * self.fric_coef

    def update(self, dt):
        friction = self.get_friction()
        # gravity = self.get_mouse_gravity()
        gravity = -1 * self.grav
        '''
        self.fri_label.text = "Fri:" + \
                          str(math.floor(friction.x))+ \
                          ', ' + \
                          str(math.floor(friction.y))

        self.acc_label.text = "Acc:" + \
                         str(math.floor(self.grav.x))+ \
                         ', ' + \
                         str(math.floor(self.grav.y))
        self.fri_label.text = "Grav: " +  str(gravity)
        '''

        self.ball.applyForce(friction)
        self.ball.applyForce(self.ball.mass * gravity)

        self.ball.checkEdge()
        self.ball.move()

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                accelerometer.enable()
                Clock.schedule_interval(self.get_acceleration, 0.05)

                self.sensorEnabled = True
                self.button.text = "Stop"
                self.startTimer = True
            else:
                accelerometer.disable()
                Clock.unschedule(self.get_acceleration)

                self.sensorEnabled = False
                self.button.text = "Start"
                self.ball.collision = 0
                self.startTimer = False

        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Accelerometer is not implemented for your platform"
            self.ids.accel_status.text = status

    def get_acceleration(self, dt):
        val = accelerometer.acceleration[:3]

        if not val == (None, None, None):
            # self.acc_label.text = "X: " + str(type(val[0]))
            # self.fri_label.text = "Y: " + str(type(val))

            self.grav.x = val[0]
            self.grav.y = val[1]


class DungeonGameApp(App):

    def build(self):
        l = Level()

        Clock.schedule_interval(l.update, 0.05)

        return l

    def on_pause(self):
        return True


if __name__ == "__main__":
    DungeonGameApp().run()