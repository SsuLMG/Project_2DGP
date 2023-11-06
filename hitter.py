from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle
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
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8











class Idle:

    @staticmethod
    def enter(hitter, e):
        hitter.frame = 0
        hitter.wait_time = get_time() # pico2d import 필요
        pass

    @staticmethod
    def exit(hitter, e):
        if space_down(e):
            hitter.fire_ball()
        pass

    @staticmethod
    def do(hitter):
        hitter.frame = (hitter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - hitter.wait_time > 2:
            hitter.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(hitter):
        hitter.image.clip_draw(int(hitter.frame) * 100, hitter.action * 100, 100, 100, hitter.x, hitter.y)


class Hit:
    @staticmethod
    def enter(hitter, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            hitter.dir, hitter.action, hitter.face_dir = 1, 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            hitter.dir, hitter.action, hitter.face_dir = -1, 0, -1

    @staticmethod
    def exit(hitter, e):
        if space_down(e):
            hitter.fire_ball()

        pass

    @staticmethod
    def do(hitter):
        # boy.frame = (boy.frame + 1) % 8
        hitter.x = 495
        hitter.y = 50
        hitter.frame = (hitter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(hitter):
        if hitter.frame == 0:
            hitter.image.clip_draw(0, 0, 40, 53, hitter.x, hitter.y)
        if hitter.frame == 1:
            hitter.image.clip_draw(40, 0, 32, 53, hitter.x, hitter.y)
        if hitter.frame == 2:
            hitter.image.clip_draw(72, 0, 57, 53, hitter.x, hitter.y)
        if hitter.frame == 3:
            hitter.image.clip_draw(129, 0, 67, 53, hitter.x, hitter.y)
        if hitter.frame == 4:
            hitter.image.clip_draw(196, 0, 62, 53, hitter.x, hitter.y)
        if hitter.frame == 5:
            hitter.image.clip_draw(258, 0, 54, 53, hitter.x, hitter.y)

#(이미지에서 x위치, y위치, 잘라낼 가로폭, 세로폭, 화면상에서 x위치 , y위치,화면상에서 출력할 이미지 가로폭, 세로폭)
# 40x53, 72x53, 129x53, 196x53, 258x53, 312x53
class StateMachine:
    def __init__(self, hitter):
        self.hitter = hitter
        self.cur_state = Idle
        self.transitions = {
            Idle: {space_down: Hit},
            Hit: {space_up: Idle}
        }

    def start(self):
        self.cur_state.enter(self.hitter, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.hitter)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.hitter, e)
                self.cur_state = next_state
                self.cur_state.enter(self.hitter, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.hitter)





class Hitter:
    def __init__(self):
        self.x, self.y = 50, 90
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('animation_sheet.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.ball_count = 10


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
        self.font.draw(self.x-10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))

    # fill here
