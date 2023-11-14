from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle
from sdl2 import SDLK_a

from ball import Ball
import game_world
import game_framework

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'




# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8











class Idle:

    @staticmethod
    def enter(pitcher, e):
        pitcher.frame = 0
        pitcher.wait_time = get_time() # pico2d import 필요
        pass

    @staticmethod
    def exit(pitcher, e):
        #if a_down(e):
        #    pitcher.fire_ball()
        pass

    @staticmethod
    def do(pitcher):
        pitcher.frame = (pitcher.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - pitcher.wait_time > 2:
            pitcher.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(pitcher):
        pitcher.image.clip_draw(0, 0, 16, 33, pitcher.x, pitcher.y,50,50)


class Pitch:
    @staticmethod
    def enter(pitcher, e):
        pitcher.frame = 0
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            pitcher.dir, pitcher.action, pitcher.face_dir = 1, 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            pitcher.dir, pitcher.action, pitcher.face_dir = -1, 0, -1

    @staticmethod
    def exit(pitcher, e):
        #if space_down(e):
        #    pitcher.fire_ball()
        pass

    @staticmethod
    def do(pitcher):
        #pitcher.frame = (pitcher.frame + 1) % 8
        pitcher.x = 576
        pitcher.y = 245
        print(pitcher.frame)
        pitcher.frame = (pitcher.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(pitcher):
        if int(pitcher.frame) == 0:
            pitcher.image.clip_draw(0, 0, 16, 33, pitcher.x, pitcher.y,50,50)
        if int(pitcher.frame) == 1:
            pitcher.image.clip_draw(16, 0, 16, 33, pitcher.x, pitcher.y,50,50)
        if int(pitcher.frame) == 2:
            pitcher.image.clip_draw(32, 0, 16, 33, pitcher.x, pitcher.y,50,50)
        if int(pitcher.frame) == 3:
            pitcher.image.clip_draw(48, 0, 15, 33, pitcher.x, pitcher.y,50,50)
        if int(pitcher.frame) == 4:
            pitcher.image.clip_draw(63, 0, 24, 33, pitcher.x, pitcher.y,50,50)
        if int(pitcher.frame) == 5:
            pitcher.image.clip_draw(87, 0, 25, 33, pitcher.x, pitcher.y,50,50)
        if int(pitcher.frame) == 6:
            pitcher.image.clip_draw(112, 0, 16, 33, pitcher.x, pitcher.y,50,50)
        if int(pitcher.frame) == 7:
            pitcher.image.clip_draw(127, 0, 18, 33, pitcher.x, pitcher.y,50,50)
        if pitcher.frame + 0.03 > 8:
            pitcher.fire_ball()

#(이미지에서 x위치, y위치, 잘라낼 가로폭, 세로폭, 화면상에서 x위치 , y위치,화면상에서 출력할 이미지 가로폭, 세로폭)
# 16x33, 32x33, 48x33, 63x33, 87x33, 112x33, 127x33, 145x33
class StateMachine:
    def __init__(self, pitcher):
        self.pitcher = pitcher
        self.cur_state = Idle
        self.transitions = {
            Idle: {a_down: Pitch},
            Pitch: {a_up: Idle}
        }

    def start(self):
        self.cur_state.enter(self.pitcher, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.pitcher)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.pitcher, e)
                self.cur_state = next_state
                self.cur_state.enter(self.pitcher, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.pitcher)





class Pitcher:
    def __init__(self):
        self.x, self.y = 576, 245
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('pitcher_animation.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.ball_count = 100


    def fire_ball(self):
        if self.ball_count > 0:
            self.ball_count -= 1
            ball = Ball(self.x, self.y, self.face_dir*10)
            game_world.add_object(ball)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        #self.font.draw(self.x-10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))

    # fill here
