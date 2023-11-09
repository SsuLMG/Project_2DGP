from pico2d import *
import game_world
import game_framework

class Ball:
    image = None

    def __init__(self, x = 495, y = 50, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity * 100 * game_framework.frame_time

        if self.x < 25 or self.x > 1172:
            game_world.remove_object(self)

        if self.y < 0 or self.y > 700:
            game_world.remove_object()

    # fill here