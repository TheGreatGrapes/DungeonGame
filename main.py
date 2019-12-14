from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.core.window import Window

class Ball(Widget):

    def __init__(self):
        super(Ball, self).__init__()
        with self.canvas:
            self.Ball = Ellipse(pos=Window.center, size=(30, 30))

class DungeonGame(App):

    def build(self):
        return Ball()


if __name__ == "__main__":
    DungeonGame().run()