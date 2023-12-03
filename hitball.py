from pico2d import *
import game_world
import random
from static import *
import game_framework
import random
import pitcher
import hitter


def Lerp(A, B, Alpha):
    return A * (1 - Alpha) + B * Alpha



class HitBall:
    image = None
    def __init__(self, x = 495, y = 50, velocity = 1):
        if HitBall.image == None:
            HitBall.image = load_image('baseball.png')
        self.x, self.y, self.velocity = x + 80, y, velocity
        self.final_ball_x = random.randint(0, 1000)  # 900
        self.final_ball_y = 500  # 230
        game_world.add_object(self)
        game_world.add_collision_pair('fielder:hitball', None, self)

    def draw(self):
        self.x = Lerp(self.x, self.final_ball_x,0.01)
        self.y = Lerp(self.y, self.final_ball_y,0.01)
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        score = Define.instance.score

        if self.x < 25 or self.x > 1100:
            game_world.remove_object(self)

        if self.y < 50 or self.y > 480:
            game_world.remove_object(self)

        if self.y >= 480:
            if self.x < 227:
                score += 500
            elif self.x >= 227 and self.x < 434:
                score += 700
            elif self.x >= 434 and self.x < 706:
                score += 1000
            elif self.x >= 706 and self.x < 904:
                score += 700
            elif self.x >= 904:
                score += 500

            Define.instance.score = score


    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10
    def handle_collision(self, group, other):
        match group:
            case 'fielder:hitball':
                game_world.remove_object(self)

    def final_x(self):
        return self.x

    def final_y(self):
        return self.y