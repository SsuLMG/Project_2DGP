from pico2d import *
import game_world
import play_mode
import game_framework
import random
import pitcher
import hitter


def Lerp(A, B, Alpha):
    return A * (1 - Alpha) + B * Alpha

final_ball_x = 940 #900
final_ball_y = 280 #230

class HitBall:
    image = None

    def __init__(self, x = 495, y = 50, velocity = 1):
        if HitBall.image == None:
            HitBall.image = load_image('baseball.png')
        self.x, self.y, self.velocity = x + 80, y, velocity

    def draw(self):
        self.x = Lerp(self.x, final_ball_x,0.01)
        self.y = Lerp(self.y, final_ball_y,0.01)
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.x < 25 or self.x > 1100:
            game_world.remove_object(self)

        if self.y < 50 or self.y > 500:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10
    def handle_collision(self, group, other):
        match group:
            case 'fielder:ball':
                game_world.remove_object(self)

    def final_x(self):
        return self.x

    def final_y(self):
        return self.y